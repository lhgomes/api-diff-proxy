from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_content_type_difference_is_reported_by_default():
    result = compare_responses(200, {"content-type":"application/json"}, b"{}", 200, {"content-type":"text/plain"}, b"{}", ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.headers.content-type"
