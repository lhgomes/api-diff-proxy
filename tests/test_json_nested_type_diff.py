from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_nested_json_type_difference_path():
    result = compare_responses(200, {}, b'{"value":{"id":1}}', 200, {}, b'{"value":[1]}', ComparisonConfig())
    assert result.differences[0].path == "$.body.value"
