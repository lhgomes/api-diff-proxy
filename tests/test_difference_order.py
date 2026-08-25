from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_dictionary_difference_order_is_stable():
    result = compare_responses(200, {}, b'{"z":1,"a":1}', 200, {}, b'{"z":2,"a":2}', ComparisonConfig())
    assert [d.path for d in result.differences] == ["$.body.a", "$.body.z"]
