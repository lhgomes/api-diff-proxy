import importlib

from fastapi.testclient import TestClient


def test_both_backend_failures_return_502(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    async def fake_call(*args, **kwargs):
        return None, 1.0, "failed"
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/test")
    assert response.status_code == 502
    assert response.headers["X-API-Diff-Result"] == "ERROR"
