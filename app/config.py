import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class BackendConfig:
    url: str


@dataclass(frozen=True)
class ComparisonConfig:
    ignore_headers: list[str] = field(default_factory=lambda: ["date", "server", "content-length"])
    ignore_json_paths: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Settings:
    primary: str
    backend_a: BackendConfig
    backend_b: BackendConfig
    timeout_seconds: float = 30.0
    comparison: ComparisonConfig = field(default_factory=ComparisonConfig)
    log_level: str = "INFO"


def _load_yaml() -> dict[str, Any]:
    path = os.getenv("CONFIG_FILE")
    if not path:
        return {}
    with Path(path).open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream) or {}


def load_settings() -> Settings:
    data = _load_yaml()
    backends = data.get("backends", {})
    comparison = data.get("comparison", {})
    proxy = data.get("proxy", {})

    primary = os.getenv("PRIMARY", data.get("primary", "backend_a")).lower()
    if primary not in {"backend_a", "backend_b"}:
        raise ValueError("PRIMARY must be backend_a or backend_b")

    backend_a_url = os.getenv("BACKEND_A_URL", backends.get("backend_a", {}).get("url", ""))
    backend_b_url = os.getenv("BACKEND_B_URL", backends.get("backend_b", {}).get("url", ""))
    if not backend_a_url or not backend_b_url:
        raise ValueError("BACKEND_A_URL and BACKEND_B_URL are required")

    return Settings(
        primary=primary,
        backend_a=BackendConfig(backend_a_url.rstrip("/")),
        backend_b=BackendConfig(backend_b_url.rstrip("/")),
        timeout_seconds=float(os.getenv("TIMEOUT_SECONDS", proxy.get("timeout_seconds", 30))),
        comparison=ComparisonConfig(
            ignore_headers=[h.lower() for h in comparison.get("ignore_headers", ["date", "server", "content-length"])],
            ignore_json_paths=list(comparison.get("ignore_json_paths", [])),
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
