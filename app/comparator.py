import json
from dataclasses import dataclass, asdict
from typing import Any

from .config import ComparisonConfig


@dataclass
class Difference:
    path: str
    backend_a: Any
    backend_b: Any


@dataclass
class ComparisonResult:
    match: bool
    differences: list[Difference]

    def as_dict(self) -> dict[str, Any]:
        return {"match": self.match, "differences": [asdict(item) for item in self.differences]}


def _remove_path(value: Any, path: str) -> None:
    # v1 intentionally supports simple JSONPath-like object paths: $.a.b.c
    if not path.startswith("$."):
        return
    parts = path[2:].split(".")
    current = value
    for part in parts[:-1]:
        if not isinstance(current, dict) or part not in current:
            return
        current = current[part]
    if isinstance(current, dict):
        current.pop(parts[-1], None)


def _diff(a: Any, b: Any, path: str, output: list[Difference]) -> None:
    if type(a) is not type(b):
        output.append(Difference(path, a, b))
        return
    if isinstance(a, dict):
        for key in sorted(set(a) | set(b)):
            child = f"{path}.{key}"
            if key not in a:
                output.append(Difference(child, None, b[key]))
            elif key not in b:
                output.append(Difference(child, a[key], None))
            else:
                _diff(a[key], b[key], child, output)
        return
    if isinstance(a, list):
        if len(a) != len(b):
            output.append(Difference(path, a, b))
            return
        for index, (left, right) in enumerate(zip(a, b)):
            _diff(left, right, f"{path}[{index}]", output)
        return
    if a != b:
        output.append(Difference(path, a, b))


def compare_responses(status_a: int, headers_a: dict[str, str], body_a: bytes,
                      status_b: int, headers_b: dict[str, str], body_b: bytes,
                      config: ComparisonConfig) -> ComparisonResult:
    differences: list[Difference] = []
    if status_a != status_b:
        differences.append(Difference("$.status", status_a, status_b))

    filtered_a = {k.lower(): v for k, v in headers_a.items() if k.lower() not in config.ignore_headers}
    filtered_b = {k.lower(): v for k, v in headers_b.items() if k.lower() not in config.ignore_headers}
    _diff(filtered_a, filtered_b, "$.headers", differences)

    try:
        json_a = json.loads(body_a)
        json_b = json.loads(body_b)
        for ignored in config.ignore_json_paths:
            _remove_path(json_a, ignored)
            _remove_path(json_b, ignored)
        _diff(json_a, json_b, "$.body", differences)
    except (json.JSONDecodeError, UnicodeDecodeError):
        if body_a != body_b:
            differences.append(Difference("$.body", body_a.decode("utf-8", "replace"), body_b.decode("utf-8", "replace")))

    return ComparisonResult(match=not differences, differences=differences)
