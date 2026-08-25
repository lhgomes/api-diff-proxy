import importlib

import httpx
from fastapi.testclient import TestClient


def test_xml_request_body_is_duplicated(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    import app.main
    module = importlib.reload(app.main)
    bodies = []
    async def fake_call(client, base_url, request, body):
        bodies.append(body)
        return httpx.Response(200, content=b"ok"), 1.0, None
    monkeypatch.setattr(module, "call_backend", fake_call)
    payload = b"<request><id>1</id></request>"
    with TestClient(module.app) as client:
        client.post("/api/xml", content=payload, headers={"content-type":"application/xml"})
    assert bodies == [payload, payload]
