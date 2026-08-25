import json

from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_property_order_is_ignored():
    result = compare_responses(200, {}, b'{"name":"John","id":123}', 200, {}, b'{"id":123,"name":"John"}', ComparisonConfig())
    assert result.match


def test_value_difference_is_reported():
    result = compare_responses(200, {}, b'{"status":"ACTIVE"}', 200, {}, b'{"status":"INACTIVE"}', ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body.status"


def test_ignored_json_path():
    config = ComparisonConfig(ignore_json_paths=["$.requestId"])
    result = compare_responses(200, {}, json.dumps({"id": 1, "requestId": "a"}).encode(), 200, {}, json.dumps({"id": 1, "requestId": "b"}).encode(), config)
    assert result.match


def test_status_difference():
    result = compare_responses(200, {}, b'{}', 404, {}, b'{}', ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.status"


def test_ignored_headers():
    config = ComparisonConfig(ignore_headers=["date"])
    result = compare_responses(200, {"date": "one"}, b'{}', 200, {"date": "two"}, b'{}', config)
    assert result.match
