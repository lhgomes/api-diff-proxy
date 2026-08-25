from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_binary_equal_with_null_bytes():
    body = b"\x00\x01\x00\x02"
    assert compare_responses(200, {}, body, 200, {}, body, ComparisonConfig()).match
