"""Persistent HTTP attempt log for honest 'verified live vs still impossible' notes."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Attempt:
    url: str
    status: str
    ok: bool
    bytes: int = 0
    content_type: str = ""
    note: str = ""
    source: str = ""
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))


class AttemptLog:
    def __init__(self) -> None:
        self.rows: list[Attempt] = []

    def add(self, **kwargs) -> Attempt:
        row = Attempt(**kwargs)
        self.rows.append(row)
        return row

    def to_dicts(self) -> list[dict]:
        return [asdict(r) for r in self.rows]

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dicts(), indent=2), encoding="utf-8")

    def markdown_table(self) -> str:
        if not self.rows:
            return "_No HTTP attempts recorded._"
        lines = [
            "| Status | OK | Bytes | Source | URL | Note |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for r in self.rows:
            url = r.url.replace("|", "%7C")
            note = (r.note or "").replace("|", "/")
            lines.append(
                f"| {r.status} | {'yes' if r.ok else 'no'} | {r.bytes:,} | {r.source} | `{url}` | {note} |"
            )
        return "\n".join(lines)
