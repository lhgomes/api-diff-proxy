from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_deep_json_difference_path():
    a = b'{"customer":{"address":{"city":"A"}}}'
    b = b'{"customer":{"address":{"city":"B"}}}'
    result = compare_responses(200, {}, a, 200, {}, b, ComparisonConfig())
    assert result.differences[0].path == "$.body.customer.address.city"
