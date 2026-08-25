from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_ignore_leaf_keeps_sibling_comparison():
    config = ComparisonConfig(ignore_json_paths=["$.meta.generatedAt"])
    a = b'{"meta":{"generatedAt":"a","version":1}}'
    b = b'{"meta":{"generatedAt":"b","version":2}}'
    result = compare_responses(200, {}, a, 200, {}, b, config)
    assert [d.path for d in result.differences] == ["$.body.meta.version"]
