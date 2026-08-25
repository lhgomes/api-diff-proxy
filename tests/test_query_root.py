from types import SimpleNamespace

import httpx
import pytest

from app.main import call_backend


class FakeClient:
    async def request(self, method, url, headers, content):
        self.url = url
        return httpx.Response(200)


@pytest.mark.asyncio
async def test_query_on_backend_root():
    client = FakeClient()
    request = SimpleNamespace(method="GET", path_params={"path": ""}, url=SimpleNamespace(query="a=1"), headers={})
    await call_backend(client, "https://backend.example.com", request, b"")
    assert client.url == "https://backend.example.com/?a=1"
