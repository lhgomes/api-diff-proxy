from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_numeric_value_difference():
    result = compare_responses(200, {}, b'{"amount":1.5}', 200, {}, b'{"amount":1.6}', ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body.amount"
