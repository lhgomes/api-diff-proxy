from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_null_and_value_differ():
    result = compare_responses(200, {}, b'{"value":null}', 200, {}, b'{"value":"x"}', ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body.value"
