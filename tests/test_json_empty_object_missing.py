from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_empty_object_and_missing_json_field_are_distinct():
    result = compare_responses(200, {}, b'{"meta":{}}', 200, {}, b'{}', ComparisonConfig())
    assert not result.match
