import importlib

import httpx
from fastapi.testclient import TestClient


def test_primary_redirect_is_returned_without_following(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        return httpx.Response(302, headers={"location": "/new-location"}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app, follow_redirects=False) as client:
        response = client.get("/api/test")
    assert response.status_code == 302
    assert response.headers["location"] == "/new-location"
