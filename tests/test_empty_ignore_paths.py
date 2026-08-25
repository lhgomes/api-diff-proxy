from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_no_ignored_paths_compares_all_json_fields():
    config = ComparisonConfig(ignore_json_paths=[])
    result = compare_responses(200, {}, b'{"requestId":"a"}', 200, {}, b'{"requestId":"b"}', config)
    assert not result.match
