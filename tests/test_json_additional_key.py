from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_additional_json_key_values_are_reported():
    result = compare_responses(200, {}, b'{"id":1,"extra":"a"}', 200, {}, b'{"id":1}', ComparisonConfig())
    diff = result.differences[0]
    assert diff.path == "$.body.extra"
    assert diff.backend_a == "a"
    assert diff.backend_b is None
