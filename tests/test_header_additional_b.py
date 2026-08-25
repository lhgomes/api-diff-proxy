from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_additional_header_on_backend_b_is_reported():
    result = compare_responses(200, {}, b"{}", 200, {"x-extra":"value"}, b"{}", ComparisonConfig())
    diff = result.differences[0]
    assert diff.backend_a is None
    assert diff.backend_b == "value"
