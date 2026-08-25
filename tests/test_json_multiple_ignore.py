from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_multiple_json_fields_can_be_ignored():
    config = ComparisonConfig(ignore_json_paths=["$.requestId", "$.timestamp"])
    a = b'{"id":1,"requestId":"a","timestamp":"x"}'
    b = b'{"timestamp":"y","requestId":"b","id":1}'
    assert compare_responses(200, {}, a, 200, {}, b, config).match
