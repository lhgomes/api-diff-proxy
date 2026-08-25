from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_list_length_difference_is_reported():
    result = compare_responses(200, {}, b'[1,2]', 200, {}, b'[1,2,3]', ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.body"
