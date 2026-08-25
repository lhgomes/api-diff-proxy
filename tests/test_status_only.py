from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_status_only_response_match():
    assert compare_responses(204, {}, b"", 204, {}, b"", ComparisonConfig()).match
