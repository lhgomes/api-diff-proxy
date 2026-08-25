from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_duplicate_keys_follow_standard_parser_behavior():
    a = b'{"id":1,"id":2}'
    b = b'{"id":2}'
    assert compare_responses(200, {}, a, 200, {}, b, ComparisonConfig()).match
