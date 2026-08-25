from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_deep_json_object_order_is_ignored():
    a = b'{"customer":{"id":1,"address":{"city":"A","zip":"1"}}}'
    b = b'{"customer":{"address":{"zip":"1","city":"A"},"id":1}}'
    assert compare_responses(200, {}, a, 200, {}, b, ComparisonConfig()).match
