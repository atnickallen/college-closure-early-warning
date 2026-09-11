"""Load config.yaml and resolve repository paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "config.yaml").exists() and (parent / "scripts").exists():
            return parent
    return Path.cwd()


@dataclass(frozen=True)
class Settings:
    raw: dict[str, Any]
    root: Path

    @property
    def years_start(self) -> int:
        return int(self.raw["years"]["start"])

    @property
    def years_end(self) -> int | None:
        end = self.raw["years"].get("end")
        return int(end) if end is not None else None

    @property
    def label_horizon_years(self) -> int:
        return int(self.raw.get("label_horizon_years", 3))

    @property
    def raw_dir(self) -> Path:
        return self.root / self.raw["paths"]["raw"]

    @property
    def processed_dir(self) -> Path:
        return self.root / self.raw["paths"]["processed"]

    @property
    def outputs_dir(self) -> Path:
        return self.root / self.raw["paths"]["outputs"]

    @property
    def urban(self) -> dict[str, Any]:
        return self.raw["urban"]

    @property
    def api_base(self) -> str:
        return self.urban["api_base"].rstrip("/")

    @property
    def csv_base(self) -> str:
        return self.urban["csv_base"].rstrip("/")

    @property
    def filters(self) -> dict[str, Any]:
        return self.raw["filters"]

    @property
    def sources(self) -> dict[str, Any]:
        return self.raw["sources"]


def load_settings(config_path: Path | None = None) -> Settings:
    root = repo_root()
    path = Path(config_path) if config_path else root / "config.yaml"
    with path.open() as fh:
        raw = yaml.safe_load(fh)
    settings = Settings(raw=raw, root=root)
    settings.raw_dir.mkdir(parents=True, exist_ok=True)
    settings.processed_dir.mkdir(parents=True, exist_ok=True)
    settings.outputs_dir.mkdir(parents=True, exist_ok=True)
    return settings
