from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_array_scalar_difference_path():
    result = compare_responses(200, {}, b'[1,2]', 200, {}, b'[1,3]', ComparisonConfig())
    assert result.differences[0].path == "$.body[1]"
