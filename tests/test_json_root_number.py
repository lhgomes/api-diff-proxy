from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_root_number_comparison():
    assert compare_responses(200, {}, b"123", 200, {}, b"123", ComparisonConfig()).match
    assert not compare_responses(200, {}, b"123", 200, {}, b"124", ComparisonConfig()).match
