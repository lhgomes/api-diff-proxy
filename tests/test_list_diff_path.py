from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_list_item_difference_path():
    result = compare_responses(200, {}, b'[{"id":1}]', 200, {}, b'[{"id":2}]', ComparisonConfig())
    assert result.differences[0].path == "$.body[0].id"
