from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_ignored_header_can_exist_on_only_one_backend():
    config = ComparisonConfig(ignore_headers=["x-request-id"])
    assert compare_responses(200, {"x-request-id":"a"}, b"{}", 200, {}, b"{}", config).match
