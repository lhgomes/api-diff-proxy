from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_decimal_json_number_difference():
    result = compare_responses(200, {}, b'{"value":1.25}', 200, {}, b'{"value":1.50}', ComparisonConfig())
    assert not result.match
