from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_whitespace_inside_json_string_is_significant():
    result = compare_responses(200, {}, b'{"value":"a b"}', 200, {}, b'{"value":"ab"}', ComparisonConfig())
    assert not result.match
