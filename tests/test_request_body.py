from types import SimpleNamespace

import httpx
import pytest

from app.main import call_backend


class FakeClient:
    def __init__(self):
        self.body = None
        self.method = None

    async def request(self, method, url, headers, content):
        self.method = method
        self.body = content
        return httpx.Response(200, content=b"ok")


@pytest.mark.asyncio
async def test_request_body_is_forwarded_unchanged():
    client = FakeClient()
    request = SimpleNamespace(method="POST", path_params={"path": "api/items"}, url=SimpleNamespace(query=""), headers={"content-type": "application/json"})
    body = b'{"value":123}'
    _, _, error = await call_backend(client, "https://backend.example.com", request, body)
    assert error is None
    assert client.method == "POST"
    assert client.body == body
