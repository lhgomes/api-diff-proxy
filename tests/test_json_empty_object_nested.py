from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_nested_empty_objects_match():
    assert compare_responses(200, {}, b'{"meta":{}}', 200, {}, b'{"meta":{}}', ComparisonConfig()).match
