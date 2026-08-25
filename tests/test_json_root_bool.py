from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_root_boolean_comparison():
    assert compare_responses(200, {}, b"true", 200, {}, b"true", ComparisonConfig()).match
    assert not compare_responses(200, {}, b"true", 200, {}, b"false", ComparisonConfig()).match
