from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_missing_json_key_is_reported():
    result = compare_responses(200, {}, b'{"id":1}', 200, {}, b'{"id":1,"name":"John"}', ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body.name"
