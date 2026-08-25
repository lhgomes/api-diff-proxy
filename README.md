# API Diff Proxy

A lightweight, API-agnostic HTTP proxy for comparing the behavior and responses of two API backends.

API Diff Proxy forwards each incoming request to two configured backends, collects both responses, compares them, and returns the response from the configured **primary backend** to the caller.

It is intended primarily for API migration, middleware replacement, regression testing, and behavioral compatibility validation.

## Overview

```text id="qfg2pe"
                         ┌──> Backend A ──> Response A ──┐
                         │                               │
Client ──> API Diff Proxy                                ├──> Compare
                         │                               │
                         └──> Backend B ──> Response B ──┘
                                                          │
                                                   Comparison Result
                                                          │
                                                          ▼
                                              Return Primary Response
```

For every incoming request, API Diff Proxy:

1. Receives the HTTP request.
2. Generates a unique comparison ID.
3. Forwards the same request to both configured backends concurrently.
4. Collects both responses.
5. Compares status codes and response bodies.
6. Records the comparison result using the comparison ID.
7. Returns the response from the configured primary backend.

The caller therefore interacts with the proxy as if it were communicating directly with the primary backend.

## API-Agnostic Proxying

API Diff Proxy is designed to operate without API-specific implementation.

The incoming:

* HTTP method
* Path
* Query string
* Request headers
* Request body

are forwarded transparently to both configured backends.

For example:

```http id="qvl0ac"
POST /api/v2/customers/123/orders?validate=true
```

can automatically be forwarded to:

```text id="i57r5w"
https://backend-a/api/v2/customers/123/orders?validate=true
https://backend-b/api/v2/customers/123/orders?validate=true
```

No code changes are required when new APIs, resources, or HTTP methods are introduced.

## Primary Backend

Either backend can be configured as the primary backend.

The primary backend determines which response is returned to the caller.

Example:

```yaml id="16h22k"
primary: backend_a

backends:
  backend_a:
    url: https://middleware-v1-dev

  backend_b:
    url: https://middleware-v2-dev
```

Changing:

```yaml id="a0t4dx"
primary: backend_b
```

makes Backend B authoritative without requiring an application change.

Both responses are still collected and compared regardless of which backend is primary.

## Use Cases

API Diff Proxy can be used to validate:

* Middleware migrations
* API rewrites
* Framework or runtime upgrades
* Cloud migrations
* Backend replacements
* API gateway changes
* Refactored services
* Legacy API modernization

The primary goal is to determine whether two implementations behave equivalently when receiving identical requests.

## Comparison Identification

Every proxied request receives a unique **comparison ID**.

The ID is included in the proxy response headers and all related structured log records, making it easy to locate the detailed comparison for a specific request.

Example response:

```http id="x4oqr7"
X-API-Diff-ID: 5fa73c32-6e27-4c28-8797-89bfcfa75e72
X-API-Diff-Result: MATCH
X-API-Diff-Primary: backend_a
```

For a mismatch:

```http id="u2tfqa"
X-API-Diff-ID: 96fbc57a-34ef-45aa-88e1-a90ad32ea02d
X-API-Diff-Result: MISMATCH
X-API-Diff-Primary: backend_a
```

The comparison ID can then be used to immediately locate the detailed request in application or container logs.

## Response Comparison

JSON responses are compared semantically rather than as raw strings.

For example, these responses are considered equivalent:

```json id="fpgdrp"
{
  "id": 123,
  "name": "John",
  "status": "ACTIVE"
}
```

```json id="zkfj40"
{
  "status": "ACTIVE",
  "name": "John",
  "id": 123
}
```

JSON property ordering therefore does not cause a mismatch.

A response such as:

```json id="kx0z0f"
{
  "id": 123,
  "name": "John",
  "status": "INACTIVE"
}
```

would produce a mismatch.

Non-JSON responses can be compared using their raw response bodies.

## Comparison Rules

Fields that are expected to differ between implementations can be excluded through configuration rather than code changes.

For example:

```yaml id="5dzn40"
comparison:
  ignore_headers:
    - date
    - server
    - x-request-id

  ignore_json_paths:
    - $.timestamp
    - $.requestId
    - $.metadata.generatedAt
```

This allows environment-specific, generated, or non-deterministic values to be excluded from comparisons.

## Configuration

The proxy is designed to require minimal configuration.

A basic configuration requires only the backend URLs and selection of the primary backend:

```yaml id="gw6ohz"
primary: backend_a

backends:
  backend_a:
    url: https://middleware-v1-dev

  backend_b:
    url: https://middleware-v2-dev

proxy:
  timeout_seconds: 30

comparison:
  ignore_headers:
    - date
    - server

  ignore_json_paths:
    - $.timestamp
    - $.requestId
```

Configuration can be supplied using environment variables and/or a configuration file.

Environment variables are suitable for container deployments where backend URLs or other settings differ between environments.

## Adding APIs

No application change should be required when a new API or resource is introduced.

For example, after the proxy is configured, all of the following can be processed automatically:

```text id="oy4q3r"
GET    /api/customers/123
POST   /api/customers
PUT    /api/customers/123
PATCH  /api/customers/123
DELETE /api/customers/123
GET    /api/orders/456/items
POST   /api/search
```

The proxy dynamically preserves the incoming method, path, query parameters, headers, and body.

API-specific configuration is only necessary when custom comparison behavior is required.

## Structured Logging

Each comparison produces a structured log entry.

Example:

```json id="4u6sk1"
{
  "comparisonId": "96fbc57a-34ef-45aa-88e1-a90ad32ea02d",
  "method": "GET",
  "path": "/api/customers/123",
  "primary": "backend_a",
  "backendA": {
    "status": 200,
    "durationMs": 124
  },
  "backendB": {
    "status": 200,
    "durationMs": 97
  },
  "match": false,
  "differences": [
    {
      "path": "$.status",
      "backendA": "ACTIVE",
      "backendB": "INACTIVE"
    }
  ]
}
```

This format is suitable for standard container logging as well as centralized logging platforms such as Azure Log Analytics.

## Planned Features

* Transparent HTTP proxying
* API-agnostic routing
* Configurable primary backend
* Concurrent requests to both backends
* Unique comparison ID for every request
* Comparison ID returned through response headers
* HTTP status comparison
* JSON-aware response comparison
* Raw/text response comparison
* Configurable JSON fields to ignore
* Configurable response headers to ignore
* Backend response-time measurements
* Structured comparison logging
* Configurable backend timeouts
* Environment-variable configuration
* Health endpoint
* Linux container support
* Azure Container Apps compatibility

## Technology

The initial implementation uses:

* Python
* FastAPI
* HTTPX
* asyncio
* Docker

The application is designed to run as a lightweight Linux container and can be deployed to Azure Container Apps, Azure Kubernetes Service, Kubernetes, or standard Docker environments.

## Project Status

Initial development.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
