from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_content_encoding_header_is_compared_by_default():
    result = compare_responses(200, {"content-encoding":"gzip"}, b"same", 200, {}, b"same", ComparisonConfig())
    assert not result.match
