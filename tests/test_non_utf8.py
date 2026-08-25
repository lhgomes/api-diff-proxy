from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_non_utf8_difference_is_reported_without_crashing():
    result = compare_responses(200, {}, bytes([255]), 200, {}, bytes([254]), ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body"
