from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_invalid_json_falls_back_to_raw_body():
    a = b'{"incomplete":'
    b = b'{"incomplete":'
    assert compare_responses(200, {}, a, 200, {}, b, ComparisonConfig()).match
