from types import SimpleNamespace

from app.main import outbound_headers


def test_request_accept_header_is_forwarded():
    request = SimpleNamespace(headers={"accept":"application/json"})
    assert outbound_headers(request)["accept"] == "application/json"
