import importlib

import httpx
from fastapi.testclient import TestClient


def test_secondary_a_failure_when_b_is_primary(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_b")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        if base_url.endswith("a.example.com"):
            return None, 1.0, "failed"
        return httpx.Response(200, json={"ok": True}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/test")
    assert response.status_code == 200
    assert response.headers["X-API-Diff-Result"] == "ERROR"
