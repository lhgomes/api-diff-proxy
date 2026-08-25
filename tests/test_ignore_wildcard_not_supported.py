from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_wildcard_jsonpath_exclusion_is_not_supported_in_v1():
    config = ComparisonConfig(ignore_json_paths=["$.items.*.id"])
    result = compare_responses(200, {}, b'{"items":{"one":{"id":1}}}', 200, {}, b'{"items":{"one":{"id":2}}}', config)
    assert not result.match
