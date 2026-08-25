import importlib

import httpx
from fastapi.testclient import TestClient


def test_arbitrary_resource_requires_no_route_configuration(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)

    paths = []
    async def fake_call(client, base_url, request, body):
        paths.append(request.path_params["path"])
        return httpx.Response(200, json={"ok": True}), 1.0, None

    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/brand/new/resource/123")
    assert response.status_code == 200
    assert paths == ["brand/new/resource/123", "brand/new/resource/123"]
