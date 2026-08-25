from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_status_header_and_body_differences_are_all_reported():
    result = compare_responses(200, {"x":"a"}, b'{"id":1}', 500, {"x":"b"}, b'{"id":2}', ComparisonConfig())
    assert [d.path for d in result.differences] == ["$.status", "$.headers.x", "$.body.id"]
