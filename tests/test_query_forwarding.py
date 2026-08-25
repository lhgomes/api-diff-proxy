from types import SimpleNamespace

import httpx
import pytest

from app.main import call_backend


class FakeClient:
    def __init__(self):
        self.url = None

    async def request(self, method, url, headers, content):
        self.url = url
        return httpx.Response(200, content=b"ok")


@pytest.mark.asyncio
async def test_query_string_is_forwarded():
    client = FakeClient()
    request = SimpleNamespace(
        method="GET",
        path_params={"path": "api/items"},
        url=SimpleNamespace(query="page=2&size=10"),
        headers={},
    )
    response, _, error = await call_backend(client, "https://backend.example.com", request, b"")
    assert error is None
    assert response.status_code == 200
    assert client.url == "https://backend.example.com/api/items?page=2&size=10"
