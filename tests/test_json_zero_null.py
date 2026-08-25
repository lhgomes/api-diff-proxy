from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_zero_and_null_json_values_are_distinct():
    result = compare_responses(200, {}, b'{"value":0}', 200, {}, b'{"value":null}', ComparisonConfig())
    assert not result.match
