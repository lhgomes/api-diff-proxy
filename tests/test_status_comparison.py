from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_status_mismatch_path():
    result = compare_responses(201, {}, b"{}", 200, {}, b"{}", ComparisonConfig())
    assert not result.match
    assert result.differences[0].path == "$.status"
    assert result.differences[0].backend_a == 201
    assert result.differences[0].backend_b == 200
