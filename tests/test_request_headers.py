from types import SimpleNamespace

from app.main import outbound_headers


def test_host_and_content_length_are_not_forwarded():
    request = SimpleNamespace(headers={"host": "proxy.example.com", "content-length": "10", "authorization": "Bearer token", "x-test": "value"})
    headers = outbound_headers(request)
    assert "host" not in headers
    assert "content-length" not in headers
    assert headers["authorization"] == "Bearer token"
    assert headers["x-test"] == "value"
