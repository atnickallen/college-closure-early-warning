"""Retrying HTTP downloads for NCES / FSA / Scorecard / WICHE files."""

from __future__ import annotations

import logging
import time
from pathlib import Path

import requests

from college_closure.attempts import AttemptLog

LOGGER = logging.getLogger(__name__)

# Browser-like UA: several FSA / ED hosts 403 a library User-Agent.
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

_GLOBAL_LOG = AttemptLog()


def attempt_log() -> AttemptLog:
    return _GLOBAL_LOG


def reset_attempt_log() -> AttemptLog:
    global _GLOBAL_LOG
    _GLOBAL_LOG = AttemptLog()
    return _GLOBAL_LOG


def download_file(
    url: str,
    dest: Path,
    *,
    timeout: int | tuple[int, int] = 180,
    max_retries: int = 4,
    backoff: float = 4.0,
    session: requests.Session | None = None,
    source: str = "",
    attempts: AttemptLog | None = None,
) -> Path | None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    log = attempts or _GLOBAL_LOG
    if dest.exists() and dest.stat().st_size > 0:
        LOGGER.info("Using cached %s (%s bytes)", dest, dest.stat().st_size)
        log.add(
            url=url,
            status="cache",
            ok=True,
            bytes=dest.stat().st_size,
            note=f"cached {dest.name}",
            source=source,
        )
        return dest
    sess = session or requests.Session()
    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            LOGGER.info("Downloading %s", url)
            with sess.get(
                url,
                headers=DEFAULT_HEADERS,
                timeout=timeout,
                stream=True,
                allow_redirects=True,
            ) as response:
                status = str(response.status_code)
                ctype = (response.headers.get("Content-Type") or "")[:80]
                if response.status_code == 404:
                    LOGGER.warning("404 %s", url)
                    log.add(url=url, status="404", ok=False, content_type=ctype, source=source)
                    return None
                if response.status_code >= 400:
                    LOGGER.warning("%s %s", response.status_code, url)
                    log.add(
                        url=url,
                        status=status,
                        ok=False,
                        content_type=ctype,
                        note=response.text[:160] if hasattr(response, "text") else "",
                        source=source,
                    )
                    response.raise_for_status()
                tmp = dest.with_suffix(dest.suffix + ".part")
                size = 0
                with tmp.open("wb") as fh:
                    for chunk in response.iter_content(1024 * 1024):
                        if chunk:
                            fh.write(chunk)
                            size += len(chunk)
                # HTML error pages sometimes arrive as 200
                if size < 800 and dest.suffix.lower() in {".zip", ".xlsx", ".xls", ".csv"}:
                    head = tmp.read_bytes()[:200].lower()
                    if b"<html" in head or b"<!doctype" in head:
                        tmp.unlink(missing_ok=True)
                        log.add(
                            url=url,
                            status="200-html",
                            ok=False,
                            bytes=size,
                            content_type=ctype,
                            note="200 but HTML body",
                            source=source,
                        )
                        return None
                tmp.replace(dest)
            LOGGER.info("Wrote %s (%s bytes)", dest, dest.stat().st_size)
            log.add(
                url=url,
                status="200",
                ok=True,
                bytes=dest.stat().st_size,
                content_type=ctype,
                source=source,
            )
            return dest
        except requests.RequestException as exc:
            last_error = exc
            sleep_for = backoff * (2 ** (attempt - 1))
            LOGGER.warning(
                "Download failed (%s/%s) %s: %s; retry in %.1fs",
                attempt,
                max_retries,
                url,
                exc,
                sleep_for,
            )
            if attempt == max_retries:
                log.add(
                    url=url,
                    status="error",
                    ok=False,
                    note=str(exc)[:240],
                    source=source,
                )
                break
            time.sleep(sleep_for)
    LOGGER.error("Giving up on %s: %s", url, last_error)
    return None


def download_first(
    urls: list[str],
    dest_dir: Path,
    stem: str,
    *,
    timeout: int | tuple[int, int] = (8, 25),
    max_retries: int = 1,
    source: str = "",
    attempts: AttemptLog | None = None,
) -> Path | None:
    """Try URLs in order; cache under dest_dir using the first successful filename."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    for url in urls:
        name = url.rstrip("/").split("/")[-1].split("?")[0] or stem
        if "." not in name:
            name = stem
        dest = dest_dir / name
        path = download_file(
            url,
            dest,
            timeout=timeout,
            max_retries=max_retries,
            backoff=1.0,
            source=source or stem,
            attempts=attempts,
        )
        if path is not None:
            return path
    LOGGER.warning("No download succeeded for %s. Tried: %s", stem, urls)
    return None


def wayback_candidates(url_pattern: str, limit: int = 15, timeout: int = 12) -> list[str]:
    """Best-effort CDX lookup. Returns raw Wayback URLs for 200 snapshots."""
    cdx = "https://web.archive.org/cdx/search/cdx"
    try:
        resp = requests.get(
            cdx,
            params={
                "url": url_pattern,
                "output": "json",
                "fl": "original,timestamp,statuscode",
                "filter": "statuscode:200",
                "limit": limit,
                "collapse": "digest",
            },
            headers=DEFAULT_HEADERS,
            timeout=timeout,
        )
        if resp.status_code >= 400:
            LOGGER.info("Wayback CDX %s for %s", resp.status_code, url_pattern)
            return []
        rows = resp.json()
    except Exception as exc:  # noqa: BLE001
        LOGGER.info("Wayback CDX skipped (%s): %s", url_pattern, exc)
        return []
    out: list[str] = []
    for row in rows[1:] if rows and isinstance(rows[0], list) else []:
        if len(row) < 2:
            continue
        original, ts = row[0], row[1]
        out.append(f"https://web.archive.org/web/{ts}id_/{original}")
    return out
