from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_raw_body_difference():
    result = compare_responses(200, {}, b"one", 200, {}, b"two", ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body"


def test_header_difference():
    result = compare_responses(200, {"x-version": "1"}, b"{}", 200, {"x-version": "2"}, b"{}", ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.headers.x-version"


def test_nested_ignored_json_path():
    config = ComparisonConfig(ignore_json_paths=["$.metadata.generatedAt"])
    result = compare_responses(200, {}, b'{"id":1,"metadata":{"generatedAt":"a"}}', 200, {}, b'{"metadata":{"generatedAt":"b"},"id":1}', config)
    assert result.match
