from types import SimpleNamespace

import httpx
import pytest

from app.main import call_backend


class FakeClient:
    def __init__(self):
        self.url = None

    async def request(self, method, url, headers, content):
        self.url = url
        return httpx.Response(200)


@pytest.mark.asyncio
async def test_nested_path_is_forwarded():
    client = FakeClient()
    request = SimpleNamespace(method="GET", path_params={"path": "api/v2/customers/123/orders"}, url=SimpleNamespace(query=""), headers={})
    _, _, error = await call_backend(client, "https://backend.example.com", request, b"")
    assert error is None
    assert client.url == "https://backend.example.com/api/v2/customers/123/orders"
