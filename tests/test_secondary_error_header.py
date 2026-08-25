import importlib

import httpx
from fastapi.testclient import TestClient


def test_secondary_error_sets_error_result_header(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        if base_url.endswith("a.example.com"):
            return httpx.Response(200, content=b"ok"), 1.0, None
        return None, 1.0, "timeout"
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/test")
    assert response.headers["X-API-Diff-Result"] == "ERROR"
    assert response.content == b"ok"
