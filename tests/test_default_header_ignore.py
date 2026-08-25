from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_default_volatile_headers_do_not_create_difference():
    config = ComparisonConfig()
    result = compare_responses(200, {"date": "a", "server": "old", "content-length": "1"}, b"{}", 200, {"date": "b", "server": "new", "content-length": "2"}, b"{}", config)
    assert result.match
