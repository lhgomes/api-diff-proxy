from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_body_detection_does_not_depend_on_content_type():
    config = ComparisonConfig(ignore_headers=["content-type"])
    a = b'{"a":1,"b":2}'
    b = b'{"b":2,"a":1}'
    result = compare_responses(200, {"content-type":"text/plain"}, a, 200, {"content-type":"application/json"}, b, config)
    assert result.match
