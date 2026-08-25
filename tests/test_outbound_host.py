from types import SimpleNamespace

from app.main import outbound_headers


def test_incoming_host_is_removed_before_forwarding():
    request = SimpleNamespace(headers={"host":"proxy.example.com", "accept":"application/json"})
    headers = outbound_headers(request)
    assert "host" not in headers
    assert headers["accept"] == "application/json"
