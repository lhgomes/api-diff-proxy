from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_ignore_path_with_scalar_parent_is_safe():
    config = ComparisonConfig(ignore_json_paths=["$.meta.value"])
    assert compare_responses(200, {}, b'{"meta":"x"}', 200, {}, b'{"meta":"x"}', config).match
