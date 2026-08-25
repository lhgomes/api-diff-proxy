import importlib

from fastapi.testclient import TestClient


def test_health_response_shape(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    with TestClient(module.app) as client:
        response = client.get("/health")
    assert response.json() == {"status": "ok"}
