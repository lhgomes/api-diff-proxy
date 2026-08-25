from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_additional_header_on_backend_a_is_reported():
    result = compare_responses(200, {"x-extra":"value"}, b"{}", 200, {}, b"{}", ComparisonConfig())
    diff = result.differences[0]
    assert diff.backend_a == "value"
    assert diff.backend_b is None
