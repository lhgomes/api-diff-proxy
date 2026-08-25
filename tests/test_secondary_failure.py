import importlib

import httpx
from fastapi.testclient import TestClient


def test_secondary_failure_still_returns_primary(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_a")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")

    import app.main
    module = importlib.reload(app.main)

    async def fake_call(client, base_url, request, body):
        if base_url == "https://a.example.com":
            return httpx.Response(200, json={"ok": True}), 10.0, None
        return None, 15.0, "connection failed"

    monkeypatch.setattr(module, "call_backend", fake_call)

    with TestClient(module.app) as client:
        response = client.get("/api/test")

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert response.headers["X-API-Diff-Result"] == "ERROR"
