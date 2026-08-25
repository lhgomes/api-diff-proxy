from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_header_values_remain_case_sensitive():
    result = compare_responses(200, {"x-test":"Value"}, b"{}", 200, {"x-test":"value"}, b"{}", ComparisonConfig())
    assert not result.match
