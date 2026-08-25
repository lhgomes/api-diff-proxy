import importlib

import httpx
from fastapi.testclient import TestClient


def test_options_request_is_proxied(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        return httpx.Response(204, headers={"allow": "GET,POST"}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.options("/api/test")
    assert response.status_code == 204
    assert response.headers["allow"] == "GET,POST"
