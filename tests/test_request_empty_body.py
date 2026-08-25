import importlib

import httpx
from fastapi.testclient import TestClient


def test_get_empty_body_is_sent_to_both_backends(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    bodies = []
    async def fake_call(client, base_url, request, body):
        bodies.append(body)
        return httpx.Response(200, content=b"ok"), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        client.get("/api/test")
    assert bodies == [b"", b""]
