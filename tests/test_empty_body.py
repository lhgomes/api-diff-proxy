from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_empty_bodies_match():
    assert compare_responses(204, {}, b"", 204, {}, b"", ComparisonConfig()).match


def test_empty_and_nonempty_body_mismatch():
    assert not compare_responses(200, {}, b"", 200, {}, b"value", ComparisonConfig()).match
