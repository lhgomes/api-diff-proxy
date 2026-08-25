from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_xml_response_uses_raw_comparison_in_v1():
    a = b"<root><id>1</id></root>"
    b = b"<root>\n<id>1</id>\n</root>"
    assert not compare_responses(200, {}, a, 200, {}, b, ComparisonConfig()).match
