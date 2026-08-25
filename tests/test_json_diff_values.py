from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_difference_contains_both_values():
    result = compare_responses(200, {}, b'{"status":"ACTIVE"}', 200, {}, b'{"status":"INACTIVE"}', ComparisonConfig())
    diff = result.differences[0]
    assert diff.backend_a == "ACTIVE"
    assert diff.backend_b == "INACTIVE"
