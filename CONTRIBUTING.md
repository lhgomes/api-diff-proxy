# Contributing

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

Set `BACKEND_A_URL`, `BACKEND_B_URL`, and optionally `PRIMARY` before running the proxy locally.

## Pull requests

Keep the proxy API-agnostic. New API resources should not require application code changes. Prefer configuration-driven comparison behavior for cases where specific response values need normalization or exclusion.

Add or update tests for behavioral changes.
