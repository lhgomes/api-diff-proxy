import importlib

from fastapi.testclient import TestClient


def test_primary_backend_failure_returns_502(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_a")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")

    import app.main
    module = importlib.reload(app.main)

    async def fake_call(client, base_url, request, body):
        if base_url == "https://a.example.com":
            return None, 10.0, "connection failed"
        return None, 10.0, "unused"

    monkeypatch.setattr(module, "call_backend", fake_call)

    with TestClient(module.app) as client:
        response = client.get("/api/test")

    assert response.status_code == 502
    assert response.headers["X-API-Diff-Result"] == "ERROR"
    assert response.headers["X-API-Diff-ID"]
