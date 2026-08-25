from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_array_jsonpath_exclusion_is_not_supported_in_v1():
    config = ComparisonConfig(ignore_json_paths=["$.items[0].id"])
    result = compare_responses(200, {}, b'{"items":[{"id":1}]}', 200, {}, b'{"items":[{"id":2}]}', config)
    assert not result.match
