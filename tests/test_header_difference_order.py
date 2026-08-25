from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_header_difference_is_reported_before_body_difference():
    result = compare_responses(200, {"x":"1"}, b'{"a":1}', 200, {"x":"2"}, b'{"a":2}', ComparisonConfig())
    assert result.differences[0].path == "$.headers.x"
    assert result.differences[1].path == "$.body.a"
