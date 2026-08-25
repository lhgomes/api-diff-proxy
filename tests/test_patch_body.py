import importlib

import httpx
from fastapi.testclient import TestClient


def test_patch_body_reaches_both_backends(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    bodies = []
    async def fake_call(client, base_url, request, body):
        bodies.append(body)
        return httpx.Response(200, json={"ok": True}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.patch("/api/test", content=b'{"name":"new"}', headers={"content-type": "application/json"})
    assert response.status_code == 200
    assert bodies == [b'{"name":"new"}', b'{"name":"new"}']
