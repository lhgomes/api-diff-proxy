from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_equivalent_json_exponent_number_semantics():
    result = compare_responses(200, {}, b'{"value":1000.0}', 200, {}, b'{"value":1e3}', ComparisonConfig())
    assert result.match
