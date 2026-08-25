from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_equivalent_json_float_formatting_matches():
    result = compare_responses(200, {}, b'{"value":1.50}', 200, {}, b'{"value":1.5}', ComparisonConfig())
    assert result.match
