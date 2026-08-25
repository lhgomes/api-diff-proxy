from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_identical_response_is_match():
    result = compare_responses(200, {"content-type": "application/json", "x-version": "1"}, b'{"ok":true}', 200, {"content-type": "application/json", "x-version": "1"}, b'{"ok":true}', ComparisonConfig())
    assert result.match
    assert result.differences == []
