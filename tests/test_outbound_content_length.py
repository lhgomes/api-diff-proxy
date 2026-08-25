from types import SimpleNamespace

from app.main import outbound_headers


def test_incoming_content_length_is_removed_before_forwarding():
    request = SimpleNamespace(headers={"content-length":"999", "content-type":"application/json"})
    headers = outbound_headers(request)
    assert "content-length" not in headers
    assert headers["content-type"] == "application/json"
