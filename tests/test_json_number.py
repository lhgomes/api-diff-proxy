from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_integer_and_float_with_same_value_are_type_sensitive():
    result = compare_responses(200, {}, b'{"value":1}', 200, {}, b'{"value":1.0}', ComparisonConfig())
    assert not result.match
