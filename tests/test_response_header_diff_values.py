from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_header_difference_contains_both_values():
    result = compare_responses(200, {"x-version":"old"}, b"{}", 200, {"x-version":"new"}, b"{}", ComparisonConfig())
    diff = result.differences[0]
    assert diff.backend_a == "old"
    assert diff.backend_b == "new"
