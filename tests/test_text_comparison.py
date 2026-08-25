from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_equal_text_bodies_match():
    assert compare_responses(200, {}, b"hello", 200, {}, b"hello", ComparisonConfig()).match


def test_text_comparison_is_exact():
    assert not compare_responses(200, {}, b"hello", 200, {}, b"Hello", ComparisonConfig()).match
