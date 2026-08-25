from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_missing_response_header_is_reported():
    result = compare_responses(200, {"x-test":"a"}, b"{}", 200, {}, b"{}", ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.headers.x-test"
