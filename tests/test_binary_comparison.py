from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_equal_binary_bodies_match():
    body = bytes([0, 255, 10, 20])
    result = compare_responses(200, {}, body, 200, {}, body, ComparisonConfig())
    assert result.match


def test_different_binary_bodies_do_not_match():
    result = compare_responses(200, {}, bytes([0, 255]), 200, {}, bytes([0, 254]), ComparisonConfig())
    assert not result.match
