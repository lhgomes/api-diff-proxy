import importlib

import httpx
from fastapi.testclient import TestClient


def test_root_path_is_proxied(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_a")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)

    async def fake_call(client, base_url, request, body):
        return httpx.Response(200, content=b"root"), 1.0, None

    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.content == b"root"
