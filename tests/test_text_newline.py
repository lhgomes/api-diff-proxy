from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_non_json_text_newline_is_significant():
    assert not compare_responses(200, {}, b"hello", 200, {}, b"hello\n", ComparisonConfig()).match
