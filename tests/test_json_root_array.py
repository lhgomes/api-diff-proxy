from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_root_json_arrays_compare_semantically_by_items():
    result = compare_responses(200, {}, b'[{"a":1,"b":2}]', 200, {}, b'[{"b":2,"a":1}]', ComparisonConfig())
    assert result.match
