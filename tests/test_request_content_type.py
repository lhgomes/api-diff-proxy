from types import SimpleNamespace

from app.main import outbound_headers


def test_request_content_type_is_forwarded():
    request = SimpleNamespace(headers={"content-type":"application/json", "host":"proxy"})
    assert outbound_headers(request)["content-type"] == "application/json"
