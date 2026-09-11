"""Urban Institute Education Data Portal client (CSV + paginated JSON API)."""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import pandas as pd
import requests

from college_closure.config import Settings

LOGGER = logging.getLogger(__name__)

YEAR_RANGE_RE = re.compile(r"(\d{4})\s*[-–—]\s*(\d{4})")
YEAR_RE = re.compile(r"\d{4}")


def parse_years_available(text: str | None) -> list[int]:
    """Parse Urban ``years_available`` strings such as ``1980, 1984–2024``."""
    if not text:
        return []
    cleaned = (
        str(text)
        .replace("&ndash;", "-")
        .replace("–", "-")
        .replace("—", "-")
        .replace("and ", ",")
    )
    years: set[int] = set()
    for match in YEAR_RANGE_RE.finditer(cleaned):
        start, end = int(match.group(1)), int(match.group(2))
        years.update(range(start, end + 1))
        cleaned = cleaned.replace(match.group(0), " ")
    for match in YEAR_RE.finditer(cleaned):
        years.add(int(match.group(0)))
    return sorted(years)


class UrbanClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "college-closure-early-warning/0.1 (+https://github.com/atnickallen/college-closure-early-warning)"
            }
        )
        self._endpoints: list[dict[str, Any]] | None = None

    @property
    def timeout(self) -> int:
        return int(self.settings.urban.get("request_timeout_seconds", 120))

    @property
    def max_retries(self) -> int:
        return int(self.settings.urban.get("max_retries", 4))

    @property
    def backoff(self) -> float:
        return float(self.settings.urban.get("retry_backoff_seconds", 4))

    def request_json(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                if response.status_code == 404:
                    return {"count": 0, "next": None, "results": [], "status_code": 404}
                response.raise_for_status()
                payload = response.json()
                if isinstance(payload, dict):
                    return payload
                return {"results": payload}
            except (requests.RequestException, ValueError) as exc:
                last_error = exc
                sleep_for = self.backoff * (2 ** (attempt - 1))
                LOGGER.warning(
                    "Request failed (%s/%s) %s: %s; retrying in %.1fs",
                    attempt,
                    self.max_retries,
                    url,
                    exc,
                    sleep_for,
                )
                time.sleep(sleep_for)
        raise RuntimeError(f"Failed after {self.max_retries} retries: {url}") from last_error

    def fetch_endpoints(self) -> list[dict[str, Any]]:
        if self._endpoints is None:
            url = f"{self.settings.api_base}/api-endpoints/"
            payload = self.request_json(url)
            self._endpoints = payload.get("results", [])
            LOGGER.info("Loaded %s Urban API endpoint metadata rows", len(self._endpoints))
        return self._endpoints

    def endpoint_meta(self, endpoint_id: int) -> dict[str, Any] | None:
        for row in self.fetch_endpoints():
            if int(row.get("endpoint_id", -1)) == int(endpoint_id):
                return row
        return None

    def years_for_endpoint(self, endpoint_id: int) -> list[int]:
        meta = self.endpoint_meta(endpoint_id)
        if not meta:
            LOGGER.warning("No Urban metadata for endpoint_id=%s", endpoint_id)
            return []
        return parse_years_available(meta.get("years_available"))

    def resolve_year_range(self, endpoint_id: int | None = None) -> list[int]:
        start = self.settings.years_start
        end = self.settings.years_end
        if end is None:
            if endpoint_id is not None:
                available = self.years_for_endpoint(endpoint_id)
                end = max(available) if available else start
            else:
                available = self.years_for_endpoint(1)  # directory
                end = max(available) if available else start
        if end < start:
            LOGGER.warning("Resolved end year %s < start %s; using start only", end, start)
            return [start]
        return list(range(start, end + 1))

    def download_csv(
        self,
        file_name: str,
        file_dir: str = "ipeds",
        dest_dir: Path | None = None,
    ) -> Path | None:
        dest_dir = dest_dir or (self.settings.raw_dir / file_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / file_name
        url = f"{self.settings.csv_base}/{file_dir}/{file_name}"
        if dest.exists() and dest.stat().st_size > 0:
            LOGGER.info("Using cached CSV %s (%s bytes)", dest, dest.stat().st_size)
            return dest

        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                LOGGER.info("Downloading %s", url)
                with self.session.get(url, stream=True, timeout=self.timeout) as response:
                    if response.status_code == 404:
                        LOGGER.warning("CSV missing (404): %s", url)
                        return None
                    response.raise_for_status()
                    tmp = dest.with_suffix(dest.suffix + ".part")
                    with tmp.open("wb") as fh:
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                fh.write(chunk)
                    tmp.replace(dest)
                LOGGER.info("Wrote %s (%s bytes)", dest, dest.stat().st_size)
                return dest
            except requests.RequestException as exc:
                last_error = exc
                sleep_for = self.backoff * (2 ** (attempt - 1))
                LOGGER.warning(
                    "CSV download failed (%s/%s) %s: %s; retrying in %.1fs",
                    attempt,
                    self.max_retries,
                    url,
                    exc,
                    sleep_for,
                )
                time.sleep(sleep_for)
        LOGGER.error("Giving up on CSV %s: %s", url, last_error)
        return None

    def fetch_api_pages(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        cache_name: str | None = None,
    ) -> pd.DataFrame:
        """Page through a JSON endpoint and optionally cache the stacked result."""
        cache_dir = self.settings.raw_dir / "ipeds" / "api_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / f"{cache_name}.parquet" if cache_name else None
        if cache_path and cache_path.exists():
            LOGGER.info("Using cached API extract %s", cache_path)
            return pd.read_parquet(cache_path)

        url = f"{self.settings.api_base}/{path.lstrip('/')}"
        if not url.endswith("/"):
            url += "/"
        query = dict(params or {})
        rows: list[dict[str, Any]] = []
        page_url = url
        page_params: dict[str, Any] | None = query or None
        pages = 0
        while page_url:
            payload = self.request_json(page_url, params=page_params)
            if payload.get("status_code") == 404 and pages == 0:
                LOGGER.warning("API path missing (404): %s params=%s", url, query)
                break
            batch = payload.get("results") or []
            rows.extend(batch)
            pages += 1
            page_url = payload.get("next")
            page_params = None  # `next` already includes query string
            if pages == 1:
                LOGGER.info(
                    "API %s count=%s first_page=%s",
                    url + (("?" + urlencode(query)) if query else ""),
                    payload.get("count"),
                    len(batch),
                )
        frame = pd.DataFrame(rows)
        if cache_path is not None:
            frame.to_parquet(cache_path, index=False)
            LOGGER.info("Cached %s rows -> %s", len(frame), cache_path)
        return frame


def read_csv_filtered(
    path: Path,
    year_min: int | None = None,
    year_max: int | None = None,
    extra_equals: dict[str, Any] | None = None,
    usecols: list[str] | None = None,
) -> pd.DataFrame:
    """Read a (possibly large) Urban CSV, optionally filtering by year / codes."""
    chunks: list[pd.DataFrame] = []
    reader = pd.read_csv(path, chunksize=200_000, low_memory=False, usecols=usecols)
    for chunk in reader:
        if year_min is not None and "year" in chunk.columns:
            chunk = chunk[chunk["year"] >= year_min]
        if year_max is not None and "year" in chunk.columns:
            chunk = chunk[chunk["year"] <= year_max]
        if extra_equals:
            for col, value in extra_equals.items():
                if col in chunk.columns:
                    chunk = chunk[chunk[col] == value]
        if not chunk.empty:
            chunks.append(chunk)
    if not chunks:
        return pd.DataFrame()
    return pd.concat(chunks, ignore_index=True)
