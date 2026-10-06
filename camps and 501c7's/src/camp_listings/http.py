"""Fetch public pages, honor robots.txt, and record blocks without raising."""

from __future__ import annotations

import ssl
from dataclasses import dataclass, field
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

USER_AGENT = "college-closure-research/1.0 (public listing check)"
_BLOCK_STATUSES = {401, 403, 429, 503}
_CHALLENGE = (
    "cf-mitigated",
    "just a moment",
    "access denied",
    "captcha",
    "akamai",
    "enable javascript and cookies",
)


@dataclass
class FetchResult:
    url: str
    status: int = 0
    body: str = ""
    final_url: str = ""
    blocked: bool = False
    reason: str = ""


@dataclass
class Client:
    user_agent: str = USER_AGENT
    timeout: int = 25
    opener: object | None = None
    _robots: dict[str, RobotFileParser | None] = field(default_factory=dict)

    def robots_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if origin not in self._robots:
            self._robots[origin] = self._load_robots(origin + "/robots.txt")
        parser = self._robots[origin]
        if parser is None:
            return True
        try:
            return bool(parser.can_fetch(self.user_agent, url))
        except Exception:
            return True

    def _load_robots(self, robots_url: str) -> RobotFileParser | None:
        try:
            status, body, _final = self._read(robots_url)
        except Exception:
            return None
        if status != 200 or not body.strip():
            return None
        parser = RobotFileParser()
        parser.parse(body.splitlines())
        return parser

    def fetch(self, url: str) -> FetchResult:
        if not self.robots_allowed(url):
            return FetchResult(url=url, blocked=True, reason="robots.txt disallows this URL")
        try:
            status, body, final = self._read(url)
        except Exception as exc:
            code = getattr(exc, "code", 0) or 0
            reason = f"HTTP {code}" if code else exc.__class__.__name__
            return FetchResult(url=url, status=int(code), blocked=True, reason=reason)
        if status in _BLOCK_STATUSES:
            return FetchResult(url=url, status=status, final_url=final, blocked=True, reason=f"HTTP {status}")
        lowered = body[:4000].lower()
        if status == 200 and any(token in lowered for token in _CHALLENGE) and len(body) < 20000:
            return FetchResult(url=url, status=status, body=body, final_url=final, blocked=True, reason="challenge page")
        if status >= 400:
            return FetchResult(url=url, status=status, final_url=final, blocked=True, reason=f"HTTP {status}")
        return FetchResult(url=url, status=status, body=body, final_url=final or url)

    def _read(self, url: str) -> tuple[int, str, str]:
        request = Request(url, headers={"User-Agent": self.user_agent})
        opener = self.opener or urlopen
        context = ssl.create_default_context()
        try:
            response = opener(request, timeout=self.timeout, context=context)
        except TypeError:
            response = opener(request, timeout=self.timeout)
        with response:
            status = int(getattr(response, "status", 200))
            final = getattr(response, "geturl", lambda: url)()
            raw = response.read()
        if isinstance(raw, str):
            text = raw
        else:
            text = raw.decode("utf-8", "replace")
        return status, text, final
