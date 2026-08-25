from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_false_and_null_json_values_are_distinct():
    result = compare_responses(200, {}, b'{"value":false}', 200, {}, b'{"value":null}', ComparisonConfig())
    assert not result.match
