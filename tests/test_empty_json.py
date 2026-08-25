from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_empty_json_objects_match():
    assert compare_responses(200, {}, b"{}", 200, {}, b"{}", ComparisonConfig()).match


def test_json_null_matches():
    assert compare_responses(200, {}, b"null", 200, {}, b"null", ComparisonConfig()).match
