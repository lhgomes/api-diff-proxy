from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_content_type_can_be_ignored():
    config = ComparisonConfig(ignore_headers=["content-type"])
    result = compare_responses(200, {"content-type":"application/json"}, b"{}", 200, {"content-type":"text/plain"}, b"{}", config)
    assert result.match
