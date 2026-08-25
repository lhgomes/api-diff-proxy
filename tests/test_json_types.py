from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_type_difference_is_reported():
    result = compare_responses(200, {}, b'{"value":1}', 200, {}, b'{"value":"1"}', ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body.value"
