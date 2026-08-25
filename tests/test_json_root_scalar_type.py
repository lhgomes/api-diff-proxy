from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_root_scalar_type_difference():
    result = compare_responses(200, {}, b'1', 200, {}, b'"1"', ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body"
