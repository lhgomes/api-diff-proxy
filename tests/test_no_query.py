from types import SimpleNamespace

import httpx
import pytest

from app.main import call_backend


class FakeClient:
    async def request(self, method, url, headers, content):
        self.url = url
        return httpx.Response(200)


@pytest.mark.asyncio
async def test_no_trailing_question_mark_without_query():
    client = FakeClient()
    request = SimpleNamespace(method="GET", path_params={"path": "items"}, url=SimpleNamespace(query=""), headers={})
    await call_backend(client, "https://backend.example.com", request, b"")
    assert client.url == "https://backend.example.com/items"
