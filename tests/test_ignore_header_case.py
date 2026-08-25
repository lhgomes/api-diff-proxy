from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_ignored_header_name_is_case_insensitive():
    config = ComparisonConfig(ignore_headers=["x-request-id"])
    result = compare_responses(200, {"X-Request-ID": "a"}, b"{}", 200, {"x-request-id": "b"}, b"{}", config)
    assert result.match
