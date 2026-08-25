from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_ignore_top_level_json_field():
    config = ComparisonConfig(ignore_json_paths=["$.timestamp"])
    result = compare_responses(200, {}, b'{"timestamp":"a","id":1}', 200, {}, b'{"timestamp":"b","id":1}', config)
    assert result.match
