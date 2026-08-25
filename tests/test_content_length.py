import importlib

import httpx
from fastapi.testclient import TestClient


def test_stale_backend_content_length_is_not_reused(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        return httpx.Response(200, content=b"abc", headers={"content-length": "999"}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/test")
    assert response.content == b"abc"
    assert response.headers["content-length"] == "3"
