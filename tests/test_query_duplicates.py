from types import SimpleNamespace

import httpx
import pytest

from app.main import call_backend


class FakeClient:
    async def request(self, method, url, headers, content):
        self.url = url
        return httpx.Response(200)


@pytest.mark.asyncio
async def test_duplicate_query_parameters_are_preserved():
    client = FakeClient()
    request = SimpleNamespace(method="GET", path_params={"path": "items"}, url=SimpleNamespace(query="id=1&id=2"), headers={})
    await call_backend(client, "https://backend.example.com", request, b"")
    assert client.url.endswith("/items?id=1&id=2")
