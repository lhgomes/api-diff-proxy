from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_unicode_semantic_match():
    a = '{"name":"João"}'.encode("utf-8")
    b = '{"name":"Jo\\u00e3o"}'.encode("utf-8")
    assert compare_responses(200, {}, a, 200, {}, b, ComparisonConfig()).match
