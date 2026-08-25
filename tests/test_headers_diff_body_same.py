from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_different_header_same_body_is_mismatch():
    result = compare_responses(200, {"x":"a"}, b'{"id":1}', 200, {"x":"b"}, b'{"id":1}', ComparisonConfig())
    assert not result.match
    assert [d.path for d in result.differences] == ["$.headers.x"]
