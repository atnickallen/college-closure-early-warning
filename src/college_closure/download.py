"""Retrying HTTP downloads for NCES / FSA files."""

from __future__ import annotations

import logging
import time
from pathlib import Path

import requests

LOGGER = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; college-closure-early-warning/0.2; "
        "+https://github.com/atnickallen/college-closure-early-warning)"
    )
}


def download_file(
    url: str,
    dest: Path,
    *,
    timeout: int = 180,
    max_retries: int = 4,
    backoff: float = 4.0,
    session: requests.Session | None = None,
) -> Path | None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        LOGGER.info("Using cached %s (%s bytes)", dest, dest.stat().st_size)
        return dest
    sess = session or requests.Session()
    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            LOGGER.info("Downloading %s", url)
            with sess.get(url, headers=DEFAULT_HEADERS, timeout=timeout, stream=True, allow_redirects=True) as response:
                if response.status_code == 404:
                    LOGGER.warning("404 %s", url)
                    return None
                response.raise_for_status()
                tmp = dest.with_suffix(dest.suffix + ".part")
                with tmp.open("wb") as fh:
                    for chunk in response.iter_content(1024 * 1024):
                        if chunk:
                            fh.write(chunk)
                tmp.replace(dest)
            LOGGER.info("Wrote %s (%s bytes)", dest, dest.stat().st_size)
            return dest
        except requests.RequestException as exc:
            last_error = exc
            sleep_for = backoff * (2 ** (attempt - 1))
            LOGGER.warning("Download failed (%s/%s) %s: %s; retry in %.1fs", attempt, max_retries, url, exc, sleep_for)
            time.sleep(sleep_for)
    LOGGER.error("Giving up on %s: %s", url, last_error)
    return None


def download_first(urls: list[str], dest_dir: Path, stem: str) -> Path | None:
    """Try URLs in order; cache under dest_dir using the first successful filename."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    for url in urls:
        name = url.rstrip("/").split("/")[-1] or stem
        dest = dest_dir / name
        path = download_file(url, dest)
        if path is not None:
            return path
    LOGGER.warning("No download succeeded for %s. Tried: %s", stem, urls)
    return None
