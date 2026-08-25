from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_non_utf8_difference_is_replacement_decoded_for_logs():
    result = compare_responses(200, {}, b"\xff", 200, {}, b"\xfe", ComparisonConfig())
    assert isinstance(result.differences[0].backend_a, str)
    assert isinstance(result.differences[0].backend_b, str)
