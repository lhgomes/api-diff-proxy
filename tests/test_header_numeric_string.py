from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_header_values_are_compared_as_strings():
    result = compare_responses(200, {"x-count":"01"}, b"{}", 200, {"x-count":"1"}, b"{}", ComparisonConfig())
    assert not result.match
