from types import SimpleNamespace

from app.main import outbound_headers


def test_conditional_request_header_is_forwarded():
    request = SimpleNamespace(headers={"if-match":"abc"})
    assert outbound_headers(request)["if-match"] == "abc"
