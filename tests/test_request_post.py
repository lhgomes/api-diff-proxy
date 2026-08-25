import importlib

import httpx
from fastapi.testclient import TestClient


def test_post_method_reaches_both_backends(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    methods = []
    async def fake_call(client, base_url, request, body):
        methods.append(request.method)
        return httpx.Response(200), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        client.post("/api/test", json={"id":1})
    assert methods == ["POST", "POST"]
