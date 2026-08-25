from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_ignored_nested_field_can_exist_on_only_one_backend():
    config = ComparisonConfig(ignore_json_paths=["$.meta.generatedAt"])
    a = b'{"id":1,"meta":{"generatedAt":"a","version":1}}'
    b = b'{"id":1,"meta":{"version":1}}'
    assert compare_responses(200, {}, a, 200, {}, b, config).match
