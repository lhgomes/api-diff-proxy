from types import SimpleNamespace

from app.main import outbound_headers


def test_custom_application_headers_are_forwarded():
    request = SimpleNamespace(headers={"x-correlation-id": "123", "x-client": "test"})
    assert outbound_headers(request) == {"x-correlation-id": "123", "x-client": "test"}
