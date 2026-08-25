from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_object_property_order_inside_array_is_ignored():
    a = b'[{"a":1,"b":2}]'
    b = b'[{"b":2,"a":1}]'
    assert compare_responses(200, {}, a, 200, {}, b, ComparisonConfig()).match
