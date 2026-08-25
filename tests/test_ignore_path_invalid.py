from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_unsupported_ignore_path_is_ignored_safely():
    config = ComparisonConfig(ignore_json_paths=["requestId"])
    result = compare_responses(200, {}, b'{"requestId":"a"}', 200, {}, b'{"requestId":"b"}', config)
    assert not result.match
