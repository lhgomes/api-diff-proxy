from types import SimpleNamespace

from app.main import outbound_headers


def test_authorization_header_is_forwarded():
    request = SimpleNamespace(headers={"authorization": "Bearer abc", "host": "proxy"})
    assert outbound_headers(request)["authorization"] == "Bearer abc"
