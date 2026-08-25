from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_empty_headers_match():
    assert compare_responses(200, {}, b"ok", 200, {}, b"ok", ComparisonConfig()).match
