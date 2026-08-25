import importlib

from fastapi.testclient import TestClient


def test_health_does_not_call_backends(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)

    async def fail_if_called(*args, **kwargs):
        raise AssertionError("backend should not be called")

    monkeypatch.setattr(module, "call_backend", fail_if_called)
    with TestClient(module.app) as client:
        response = client.get("/health")
    assert response.status_code == 200
