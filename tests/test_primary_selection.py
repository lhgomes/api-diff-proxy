import importlib

import httpx
from fastapi.testclient import TestClient


def test_backend_b_can_be_primary(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_b")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")

    import app.main
    module = importlib.reload(app.main)

    async def fake_call(client, base_url, request, body):
        if base_url == "https://a.example.com":
            return httpx.Response(200, json={"source": "a"}), 10.0, None
        return httpx.Response(201, json={"source": "b"}), 12.0, None

    monkeypatch.setattr(module, "call_backend", fake_call)

    with TestClient(module.app) as client:
        response = client.post("/api/test", json={"value": 1})

    assert response.status_code == 201
    assert response.json() == {"source": "b"}
    assert response.headers["X-API-Diff-Primary"] == "backend_b"
    assert response.headers["X-API-Diff-Result"] == "MISMATCH"
