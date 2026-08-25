from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_nested_empty_arrays_match():
    assert compare_responses(200, {}, b'{"items":[]}', 200, {}, b'{"items":[]}', ComparisonConfig()).match
