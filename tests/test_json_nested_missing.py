from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_nested_missing_json_field_path():
    result = compare_responses(200, {}, b'{"customer":{"id":1}}', 200, {}, b'{"customer":{"id":1,"name":"John"}}', ComparisonConfig())
    assert result.differences[0].path == "$.body.customer.name"
