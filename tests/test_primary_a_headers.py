import importlib

import httpx
from fastapi.testclient import TestClient


def test_backend_a_headers_are_authoritative_by_default(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.delenv("PRIMARY", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(client, base_url, request, body):
        source = "a" if base_url.endswith("a.example.com") else "b"
        return httpx.Response(200, content=b"ok", headers={"x-source":source}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/test")
    assert response.headers["x-source"] == "a"
