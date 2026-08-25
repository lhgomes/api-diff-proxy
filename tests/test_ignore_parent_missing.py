from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_ignore_path_with_missing_parent_is_safe():
    config = ComparisonConfig(ignore_json_paths=["$.missing.value"])
    assert compare_responses(200, {}, b'{"id":1}', 200, {}, b'{"id":1}', config).match
