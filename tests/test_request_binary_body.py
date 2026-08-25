import importlib

import httpx
from fastapi.testclient import TestClient


def test_binary_request_body_is_duplicated_unchanged(monkeypatch):
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
    payload = bytes([0, 255, 1, 2])
    with TestClient(module.app) as client:
        client.post("/api/upload", content=payload)
    assert bodies == [payload, payload]
