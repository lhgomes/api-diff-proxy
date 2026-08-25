import importlib

import httpx
from fastapi.testclient import TestClient


def test_secondary_error_does_not_modify_primary_body(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        if base_url.endswith("a.example.com"):
            return httpx.Response(200, content=b"primary"), 1.0, None
        return None, 1.0, "failed"
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/test")
    assert response.content == b"primary"
