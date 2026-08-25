from types import SimpleNamespace

from app.main import outbound_headers


def test_trace_context_header_is_forwarded():
    request = SimpleNamespace(headers={"traceparent":"00-abc-def-01"})
    assert outbound_headers(request)["traceparent"] == "00-abc-def-01"
