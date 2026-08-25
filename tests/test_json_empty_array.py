from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_empty_json_arrays_match():
    assert compare_responses(200, {}, b"[]", 200, {}, b"[]", ComparisonConfig()).match
