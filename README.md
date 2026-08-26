# API Diff Proxy

A lightweight, API-agnostic HTTP proxy that sends the same request to two backends, compares their responses, and returns the response from a configurable primary backend.

Designed for middleware migrations, API rewrites, regression testing, and behavioral compatibility validation.

## How it works

```text
                         +--> Backend A --> Response A --+
                         |                                |
Client --> API Diff Proxy                                +--> Compare
                         |                                |
                         +--> Backend B --> Response B --+
                                                          |
                                               Return primary response
```

For each request the proxy generates a comparison ID, forwards method/path/query/headers/body concurrently to both backends, compares the responses, writes a structured JSON log to stdout, and returns the configured primary response.

The response includes:

```http
X-API-Diff-ID: 96fbc57a-34ef-45aa-88e1-a90ad32ea02d
X-API-Diff-Result: MATCH
X-API-Diff-Primary: backend_a
```

Use `X-API-Diff-ID` to find the detailed comparison in container logs.

## Configuration

No API/resource definitions are required. New resources are proxied automatically.

### Environment variables

```text
PRIMARY=backend_a
BACKEND_A_URL=https://middleware-v1-dev.example.com
BACKEND_B_URL=https://middleware-v2-dev.example.com
```

These are the only required settings. Optional settings:

```text
TIMEOUT_SECONDS=30
LOG_LEVEL=INFO
CONFIG_FILE=/app/config.yaml
```

`PRIMARY` can be `backend_a` or `backend_b` and determines which backend response is returned to the caller.

### YAML configuration

The application does not automatically load `config.yaml`. To use YAML-defined
backends, comparison rules, or proxy settings, provide the file path through
`CONFIG_FILE` before starting the application:

```yaml
primary: backend_a

backends:
  backend_a:
    url: https://middleware-v1-dev.example.com
  backend_b:
    url: https://middleware-v2-dev.example.com

proxy:
  timeout_seconds: 30

comparison:
  ignore_headers:
    - date
    - server
    - content-length
  ignore_json_paths:
    - $.timestamp
    - $.requestId
```

Environment variables override the corresponding YAML values.

## Comparison behavior

The proxy compares HTTP status, response headers, and response body. JSON is compared semantically, so object property order does not matter. Non-JSON bodies use raw comparison.

Simple JSON object paths such as `$.requestId` and `$.metadata.generatedAt` can be excluded. Array/wildcard JSONPath expressions are not supported in the initial version.

By default the volatile `date`, `server`, and `content-length` headers are ignored.

## Logging

No logging destination configuration is required. One structured JSON comparison record is emitted to stdout for each request. Docker, Azure Container Apps, Kubernetes, or another container platform can collect and ship these logs.

Example:

```json
{"comparisonId":"96fbc57a-34ef-45aa-88e1-a90ad32ea02d","method":"GET","path":"/api/customers/123","primary":"backend_a","backendA":{"status":200,"durationMs":124.0,"error":null},"backendB":{"status":200,"durationMs":97.0,"error":null},"result":"MISMATCH","differences":[{"path":"$.body.status","backend_a":"ACTIVE","backend_b":"INACTIVE"}]}
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PRIMARY=backend_a
export BACKEND_A_URL=https://middleware-v1-dev.example.com
export BACKEND_B_URL=https://middleware-v2-dev.example.com
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

To load the example YAML config shipped with the repository (`config.example.yaml`), start it with:

    CONFIG_FILE="$PWD/config.example.yaml" uvicorn app.main:app --host 0.0.0.0 --port 8080

Health check:

```text
GET /health
```

## Docker

```bash
docker build -t api-diff-proxy .

docker run --rm -p 8080:8080 \
  -v "$PWD/config.yaml:/app/config.yaml:ro" \
  -e CONFIG_FILE=/app/config.yaml \
  -e PRIMARY=backend_a \
  -e BACKEND_A_URL=https://middleware-v1-dev.example.com \
  -e BACKEND_B_URL=https://middleware-v2-dev.example.com \
  api-diff-proxy
```

The image runs as a non-root user and exposes port `8080`.

## Development

```bash
pip install -r requirements-dev.txt
pytest -q
```

GitHub Actions runs the test suite and validates the Docker build for pull requests.

## Technology

- Python 3.13
- FastAPI
- HTTPX
- asyncio
- Docker

## License

MIT. See [LICENSE](LICENSE).
