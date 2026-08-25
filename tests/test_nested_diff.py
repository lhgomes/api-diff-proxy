from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_nested_difference_path():
    result = compare_responses(200, {}, b'{"customer":{"status":"ACTIVE"}}', 200, {}, b'{"customer":{"status":"INACTIVE"}}', ComparisonConfig())
    assert result.differences[0].path == "$.body.customer.status"
