import importlib

from fastapi.testclient import TestClient


def test_health_does_not_add_diff_headers(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    with TestClient(module.app) as client:
        response = client.get("/health")
    assert "X-API-Diff-ID" not in response.headers
