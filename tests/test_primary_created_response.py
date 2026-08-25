import importlib

import httpx
from fastapi.testclient import TestClient


def test_created_primary_response(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        return httpx.Response(201, json={"id":1}, headers={"location":"/api/items/1"}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.post("/api/items", json={"name":"test"})
    assert response.status_code == 201
    assert response.json() == {"id":1}
