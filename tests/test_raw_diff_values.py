from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_raw_difference_contains_text_values():
    result = compare_responses(200, {}, b"old", 200, {}, b"new", ComparisonConfig())
    diff = result.differences[0]
    assert diff.backend_a == "old"
    assert diff.backend_b == "new"
