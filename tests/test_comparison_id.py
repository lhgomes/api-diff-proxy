import importlib
import uuid

import httpx
from fastapi.testclient import TestClient


def test_comparison_id_is_uuid(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_a")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)

    async def fake_call(client, base_url, request, body):
        return httpx.Response(200, json={"ok": True}), 1.0, None

    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/test")
    uuid.UUID(response.headers["X-API-Diff-ID"])
