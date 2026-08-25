from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_boolean_difference():
    result = compare_responses(200, {}, b'{"enabled":true}', 200, {}, b'{"enabled":false}', ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body.enabled"
