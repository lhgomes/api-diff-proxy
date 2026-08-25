from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_status_and_header_differences_are_collected():
    result = compare_responses(200, {"x":"1"}, b"{}", 201, {"x":"2"}, b"{}", ComparisonConfig())
    assert {d.path for d in result.differences} == {"$.status", "$.headers.x"}
