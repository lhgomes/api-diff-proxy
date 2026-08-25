from types import SimpleNamespace

from app.main import outbound_headers


def test_request_user_agent_is_forwarded():
    request = SimpleNamespace(headers={"user-agent":"test-client"})
    assert outbound_headers(request)["user-agent"] == "test-client"
