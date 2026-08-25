from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_status_difference_is_reported_before_body_difference():
    result = compare_responses(200, {}, b'{"a":1}', 500, {}, b'{"a":2}', ComparisonConfig())
    assert result.differences[0].path == "$.status"
