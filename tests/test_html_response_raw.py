from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_html_response_uses_raw_comparison():
    assert not compare_responses(200, {}, b"<p>Hello</p>", 200, {}, b"<p>hello</p>", ComparisonConfig()).match
