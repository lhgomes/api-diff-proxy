import importlib

import httpx
from fastapi.testclient import TestClient


def load_app(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_a")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    return importlib.reload(app.main)


def test_health(monkeypatch):
    module = load_app(monkeypatch)
    with TestClient(module.app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_primary_response_and_diff_headers(monkeypatch):
    module = load_app(monkeypatch)

    async def fake_call(client, base_url, request, body):
        if base_url == "https://a.example.com":
            return httpx.Response(200, json={"id": 1, "status": "ACTIVE"}), 10.0, None
        return httpx.Response(200, json={"status": "ACTIVE", "id": 1}), 12.0, None

    monkeypatch.setattr(module, "call_backend", fake_call)

    with TestClient(module.app) as client:
        response = client.get("/api/customers/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "status": "ACTIVE"}
    assert response.headers["X-API-Diff-Result"] == "MATCH"
    assert response.headers["X-API-Diff-Primary"] == "backend_a"
    assert response.headers["X-API-Diff-ID"]
