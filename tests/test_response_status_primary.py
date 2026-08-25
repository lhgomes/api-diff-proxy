import importlib

import httpx
from fastapi.testclient import TestClient


def test_primary_status_code_is_returned(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_a")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        status = 404 if base_url.endswith("a.example.com") else 200
        return httpx.Response(status, json={"status": status}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/missing")
    assert response.status_code == 404
    assert response.headers["X-API-Diff-Result"] == "MISMATCH"
