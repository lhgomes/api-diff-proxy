from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_nested_array_difference_path():
    a = b'{"items":[{"value":1}]}'
    b = b'{"items":[{"value":2}]}'
    result = compare_responses(200, {}, a, 200, {}, b, ComparisonConfig())
    assert result.differences[0].path == "$.body.items[0].value"
