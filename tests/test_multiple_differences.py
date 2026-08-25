from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_multiple_json_differences_are_collected():
    result = compare_responses(200, {}, b'{"a":1,"b":2}', 200, {}, b'{"a":3,"b":4}', ComparisonConfig())
    assert not result.match
    assert {item.path for item in result.differences} == {"$.body.a", "$.body.b"}
