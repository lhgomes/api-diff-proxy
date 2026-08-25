from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_list_length_difference_contains_lists():
    result = compare_responses(200, {}, b'[1]', 200, {}, b'[1,2]', ComparisonConfig())
    diff = result.differences[0]
    assert diff.backend_a == [1]
    assert diff.backend_b == [1, 2]
