from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_ignore_paths_are_case_sensitive():
    config = ComparisonConfig(ignore_json_paths=["$.requestId"])
    result = compare_responses(200, {}, b'{"RequestId":"a"}', 200, {}, b'{"RequestId":"b"}', config)
    assert not result.match
