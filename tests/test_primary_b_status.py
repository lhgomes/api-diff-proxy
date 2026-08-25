import importlib

import httpx
from fastapi.testclient import TestClient


def test_backend_b_status_is_authoritative_when_primary(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_b")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        status = 200 if base_url.endswith("a.example.com") else 202
        return httpx.Response(status, content=b"ok"), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.post("/api/test")
    assert response.status_code == 202
