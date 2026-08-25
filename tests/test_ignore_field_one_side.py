from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_ignored_field_can_exist_on_only_one_backend():
    config = ComparisonConfig(ignore_json_paths=["$.requestId"])
    result = compare_responses(200, {}, b'{"id":1,"requestId":"a"}', 200, {}, b'{"id":1}', config)
    assert result.match
