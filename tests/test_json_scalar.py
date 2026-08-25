from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_scalar_values_compare():
    assert compare_responses(200, {}, b'"value"', 200, {}, b'"value"', ComparisonConfig()).match
    assert not compare_responses(200, {}, b'"value"', 200, {}, b'"other"', ComparisonConfig()).match
