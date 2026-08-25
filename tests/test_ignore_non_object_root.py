from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_object_path_exclusion_on_array_root_is_safe():
    config = ComparisonConfig(ignore_json_paths=["$.requestId"])
    assert compare_responses(200, {}, b'[1]', 200, {}, b'[1]', config).match
