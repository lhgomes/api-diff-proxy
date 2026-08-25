from types import SimpleNamespace

from app.main import outbound_headers


def test_request_cookie_header_is_forwarded():
    request = SimpleNamespace(headers={"cookie":"session=abc"})
    assert outbound_headers(request)["cookie"] == "session=abc"
