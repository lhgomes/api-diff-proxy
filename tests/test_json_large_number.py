from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_large_json_integer_comparison():
    value = b'{"id":12345678901234567890}'
    assert compare_responses(200, {}, value, 200, {}, value, ComparisonConfig()).match
