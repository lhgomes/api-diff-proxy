from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_root_jsonpath_exclusion_is_not_supported_in_v1():
    config = ComparisonConfig(ignore_json_paths=["$"])
    result = compare_responses(200, {}, b'{"id":1}', 200, {}, b'{"id":2}', config)
    assert not result.match
