from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_same_status_different_body_is_mismatch():
    result = compare_responses(200, {}, b'{"id":1}', 200, {}, b'{"id":2}', ComparisonConfig())
    assert not result.match
    assert all(d.path != "$.status" for d in result.differences)
