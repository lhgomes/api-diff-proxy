from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_ignored_field_does_not_hide_other_difference():
    config = ComparisonConfig(ignore_json_paths=["$.requestId"])
    a = b'{"requestId":"a","status":"ACTIVE"}'
    b = b'{"requestId":"b","status":"INACTIVE"}'
    result = compare_responses(200, {}, a, 200, {}, b, config)
    assert [item.path for item in result.differences] == ["$.body.status"]
