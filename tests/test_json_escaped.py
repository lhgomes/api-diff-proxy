from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_equivalent_json_escape_sequences_match():
    a = b'{"path":"a/b"}'
    b = b'{"path":"a\\/b"}'
    assert compare_responses(200, {}, a, 200, {}, b, ComparisonConfig()).match
