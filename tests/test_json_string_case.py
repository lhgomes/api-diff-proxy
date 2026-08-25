from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_json_string_values_are_case_sensitive():
    result = compare_responses(200, {}, b'{"status":"ACTIVE"}', 200, {}, b'{"status":"active"}', ComparisonConfig())
    assert not result.match
