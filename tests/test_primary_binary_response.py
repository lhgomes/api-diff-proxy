import importlib

import httpx
from fastapi.testclient import TestClient


def test_primary_binary_response_is_returned_unchanged(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    payload = bytes([0, 255, 1, 2])
    async def fake_call(client, base_url, request, body):
        return httpx.Response(200, content=payload, headers={"content-type":"application/octet-stream"}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/file")
    assert response.content == payload
