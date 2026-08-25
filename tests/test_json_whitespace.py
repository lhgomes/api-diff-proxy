from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_whitespace_is_ignored():
    result = compare_responses(200, {}, b'{"id":1,"name":"John"}', 200, {}, b'{\n  "id": 1,\n  "name": "John"\n}', ComparisonConfig())
    assert result.match
