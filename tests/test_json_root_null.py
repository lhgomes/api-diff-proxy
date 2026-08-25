from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_root_null_comparison():
    assert compare_responses(200, {}, b"null", 200, {}, b"null", ComparisonConfig()).match
    assert not compare_responses(200, {}, b"null", 200, {}, b"0", ComparisonConfig()).match
