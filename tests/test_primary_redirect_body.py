import importlib

import httpx
from fastapi.testclient import TestClient


def test_redirect_primary_body_is_preserved(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        return httpx.Response(307, content=b"redirect", headers={"location":"/new"}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app, follow_redirects=False) as client:
        response = client.post("/api/old")
    assert response.status_code == 307
    assert response.content == b"redirect"
