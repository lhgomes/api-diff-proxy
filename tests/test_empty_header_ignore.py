from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_no_ignored_headers_compares_all_headers():
    config = ComparisonConfig(ignore_headers=[])
    result = compare_responses(200, {"date":"a"}, b"{}", 200, {"date":"b"}, b"{}", config)
    assert not result.match
