import importlib

import httpx
from fastapi.testclient import TestClient


def test_bad_request_primary_response(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        return httpx.Response(400, json={"error":"invalid"}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.post("/api/test")
    assert response.status_code == 400
    assert response.json() == {"error":"invalid"}
