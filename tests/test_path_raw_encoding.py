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
async def test_encoded_path_is_forwarded_verbatim():
    client = FakeClient()
    request = SimpleNamespace(
        method="GET",
        path_params={"path": "api/a/b"},
        url=SimpleNamespace(query=""),
        headers={},
        scope={"raw_path": b"/api/a%2Fb"},
    )
    await call_backend(client, "https://backend.example.com", request, b"")
    assert client.url == "https://backend.example.com/api/a%2Fb"


@pytest.mark.asyncio
async def test_path_params_fallback_without_scope():
    client = FakeClient()
    request = SimpleNamespace(
        method="GET",
        path_params={"path": "api/items"},
        url=SimpleNamespace(query=""),
        headers={},
    )
    await call_backend(client, "https://backend.example.com", request, b"")
    assert client.url == "https://backend.example.com/api/items"
