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
async def test_existing_query_encoding_is_preserved():
    client = FakeClient()
    request = SimpleNamespace(method="GET", path_params={"path": "search"}, url=SimpleNamespace(query="q=hello%20world&x=a%2Fb"), headers={})
    await call_backend(client, "https://backend.example.com", request, b"")
    assert client.url.endswith("/search?q=hello%20world&x=a%2Fb")
