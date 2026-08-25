from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_array_element_order_remains_significant():
    result = compare_responses(200, {}, b'[{"id":1},{"id":2}]', 200, {}, b'[{"id":2},{"id":1}]', ComparisonConfig())
    assert not result.match
