import importlib

import httpx
from fastapi.testclient import TestClient


def test_header_mismatch_does_not_change_primary_header(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        source = "primary" if base_url.endswith("a.example.com") else "secondary"
        return httpx.Response(200, content=b"ok", headers={"x-source":source}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/test")
    assert response.headers["x-source"] == "primary"
    assert response.headers["X-API-Diff-Result"] == "MISMATCH"
