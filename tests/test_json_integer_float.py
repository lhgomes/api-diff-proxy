from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_integer_and_float_json_types_are_distinct_in_v1():
    result = compare_responses(200, {}, b'{"value":1}', 200, {}, b'{"value":1.0}', ComparisonConfig())
    assert not result.match
