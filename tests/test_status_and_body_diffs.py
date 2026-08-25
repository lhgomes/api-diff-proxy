from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_status_and_body_differences_are_both_reported():
    result = compare_responses(200, {}, b'{"ok":true}', 500, {}, b'{"ok":false}', ComparisonConfig())
    paths = {item.path for item in result.differences}
    assert "$.status" in paths
    assert "$.body.ok" in paths
