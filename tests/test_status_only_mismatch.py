from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_status_only_response_mismatch():
    result = compare_responses(204, {}, b"", 404, {}, b"", ComparisonConfig())
    assert not result.match
    assert len(result.differences) == 1
