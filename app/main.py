import asyncio
import json
import logging
import time
import uuid
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from .comparator import compare_responses
from .config import load_settings

settings = load_settings()
logging.basicConfig(level=settings.log_level, format="%(message)s")
logger = logging.getLogger("api-diff-proxy")

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}
PROXY_RESPONSE_HEADERS = {
    "x-api-diff-id",
    "x-api-diff-result",
    "x-api-diff-primary",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=settings.timeout_seconds, follow_redirects=False)
    yield
    await app.state.client.aclose()


app = FastAPI(title="API Diff Proxy", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


def _connection_tokens(headers) -> set[str]:
    value = headers.get("connection", "")
    return {token.strip().lower() for token in value.split(",") if token.strip()}


def outbound_headers(request: Request) -> dict[str, str]:
    excluded = HOP_BY_HOP_HEADERS | _connection_tokens(request.headers) | {"host", "content-length"}
    return {key: value for key, value in request.headers.items() if key.lower() not in excluded}


def response_headers(response: httpx.Response) -> dict[str, str]:
    excluded = (
        HOP_BY_HOP_HEADERS
        | _connection_tokens(response.headers)
        | PROXY_RESPONSE_HEADERS
        | {"content-length"}
    )
    return {key: value for key, value in response.headers.items() if key.lower() not in excluded}


async def call_backend(client: httpx.AsyncClient, base_url: str, request: Request, body: bytes):
    url = f"{base_url}/{request.path_params.get('path', '')}"
    if request.url.query:
        url = f"{url}?{request.url.query}"
    started = time.perf_counter()
    try:
        response = await client.request(request.method, url, headers=outbound_headers(request), content=body)
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        return response, duration_ms, None
    except httpx.HTTPError as exc:
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        return None, duration_ms, str(exc)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def proxy(request: Request, path: str):
    comparison_id = str(uuid.uuid4())
    body = await request.body()
    result_a, result_b = await asyncio.gather(
        call_backend(request.app.state.client, settings.backend_a.url, request, body),
        call_backend(request.app.state.client, settings.backend_b.url, request, body),
    )
    response_a, duration_a, error_a = result_a
    response_b, duration_b, error_b = result_b

    primary_response = response_a if settings.primary == "backend_a" else response_b
    primary_error = error_a if settings.primary == "backend_a" else error_b

    if primary_response is None:
        logger.error(json.dumps({"comparisonId": comparison_id, "result": "ERROR", "primary": settings.primary, "error": primary_error}))
        return JSONResponse(
            status_code=502,
            content={"detail": "Primary backend request failed", "comparisonId": comparison_id},
            headers={
                "X-API-Diff-ID": comparison_id,
                "X-API-Diff-Result": "ERROR",
                "X-API-Diff-Primary": settings.primary,
            },
        )

    if response_a is None or response_b is None:
        comparison_result = "ERROR"
        differences = []
    else:
        compared = compare_responses(
            response_a.status_code,
            dict(response_a.headers),
            response_a.content,
            response_b.status_code,
            dict(response_b.headers),
            response_b.content,
            settings.comparison,
        )
        comparison_result = "MATCH" if compared.match else "MISMATCH"
        differences = compared.as_dict()["differences"]

    log_record = {
        "comparisonId": comparison_id,
        "method": request.method,
        "path": request.url.path,
        "query": request.url.query,
        "primary": settings.primary,
        "backendA": {"status": response_a.status_code if response_a else None, "durationMs": duration_a, "error": error_a},
        "backendB": {"status": response_b.status_code if response_b else None, "durationMs": duration_b, "error": error_b},
        "result": comparison_result,
        "differences": differences,
    }
    logger.info(json.dumps(log_record, default=str, separators=(",", ":")))

    headers = response_headers(primary_response)
    headers.update(
        {
            "X-API-Diff-ID": comparison_id,
            "X-API-Diff-Result": comparison_result,
            "X-API-Diff-Primary": settings.primary,
        }
    )
    return Response(content=primary_response.content, status_code=primary_response.status_code, headers=headers)
