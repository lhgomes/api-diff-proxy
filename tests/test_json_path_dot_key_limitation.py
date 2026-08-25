from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_keys_containing_dots_are_not_addressable_by_v1_ignore_paths():
    config = ComparisonConfig(ignore_json_paths=["$.meta.generated.at"])
    a = b'{"meta":{"generated.at":"a"}}'
    b = b'{"meta":{"generated.at":"b"}}'
    assert not compare_responses(200, {}, a, 200, {}, b, config).match
