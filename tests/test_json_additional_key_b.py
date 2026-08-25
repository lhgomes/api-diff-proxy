from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_additional_json_key_on_backend_b_is_reported():
    result = compare_responses(200, {}, b'{"id":1}', 200, {}, b'{"id":1,"extra":"b"}', ComparisonConfig())
    diff = result.differences[0]
    assert diff.path == "$.body.extra"
    assert diff.backend_a is None
    assert diff.backend_b == "b"
