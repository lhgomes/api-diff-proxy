from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_header_names_are_case_insensitive():
    result = compare_responses(200, {"X-Test": "value"}, b"{}", 200, {"x-test": "value"}, b"{}", ComparisonConfig())
    assert result.match
