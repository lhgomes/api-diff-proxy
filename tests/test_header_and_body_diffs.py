from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_header_and_body_differences_are_both_reported():
    result = compare_responses(200, {"x-version":"1"}, b'{"ok":true}', 200, {"x-version":"2"}, b'{"ok":false}', ComparisonConfig())
    paths = {item.path for item in result.differences}
    assert "$.headers.x-version" in paths
    assert "$.body.ok" in paths
