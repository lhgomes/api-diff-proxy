import importlib

import httpx
from fastapi.testclient import TestClient


def test_primary_json_bytes_are_returned_without_reformatting(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    primary = b'{"z":1,"a":2}'
    async def fake_call(client, base_url, request, body):
        content = primary if base_url.endswith("a.example.com") else b'{"a":2,"z":1}'
        return httpx.Response(200, content=content, headers={"content-type":"application/json"}), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    with TestClient(module.app) as client:
        response = client.get("/api/test")
    assert response.content == primary
    assert response.headers["X-API-Diff-Result"] == "MATCH"
