from types import SimpleNamespace

import httpx
import pytest

from app.main import call_backend


class TimeoutClient:
    async def request(self, method, url, headers, content):
        raise httpx.TimeoutException("timed out")


@pytest.mark.asyncio
async def test_backend_timeout_is_captured():
    request = SimpleNamespace(method="GET", path_params={"path": "api/test"}, url=SimpleNamespace(query=""), headers={})
    response, duration, error = await call_backend(TimeoutClient(), "https://backend.example.com", request, b"")
    assert response is None
    assert duration >= 0
    assert "timed out" in error
