from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_nested_ignored_field_is_removed_from_both_responses():
    config = ComparisonConfig(ignore_json_paths=["$.meta.request.id"])
    a = b'{"value":1,"meta":{"request":{"id":"a","type":"x"}}}'
    b = b'{"meta":{"request":{"type":"x","id":"b"}},"value":1}'
    assert compare_responses(200, {}, a, 200, {}, b, config).match
