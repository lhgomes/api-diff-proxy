import importlib

import httpx
import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
def test_supported_http_methods(monkeypatch, method):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_a")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")

    import app.main
    module = importlib.reload(app.main)

    async def fake_call(client, base_url, request, body):
        return httpx.Response(204), 1.0, None

    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.request(method, "/api/test")
    assert response.status_code == 204
