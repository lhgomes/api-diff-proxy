from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_boolean_and_integer_json_types_are_distinct():
    result = compare_responses(200, {}, b'{"value":true}', 200, {}, b'{"value":1}', ComparisonConfig())
    assert not result.match
