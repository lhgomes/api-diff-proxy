from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_multiple_custom_headers_can_be_ignored():
    config = ComparisonConfig(ignore_headers=["x-request-id", "x-generated-at"])
    a = {"x-request-id":"1", "x-generated-at":"a", "x-version":"same"}
    b = {"x-request-id":"2", "x-generated-at":"b", "x-version":"same"}
    assert compare_responses(200, a, b"{}", 200, b, b"{}", config).match
