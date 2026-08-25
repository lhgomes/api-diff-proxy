from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_array_order_is_significant():
    result = compare_responses(200, {}, b'[1,2,3]', 200, {}, b'[3,2,1]', ComparisonConfig())
    assert not result.match


def test_equal_json_arrays_match():
    result = compare_responses(200, {}, b'[{"id":1},{"id":2}]', 200, {}, b'[{"id":1},{"id":2}]', ComparisonConfig())
    assert result.match
