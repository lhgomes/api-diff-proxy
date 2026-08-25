from app.comparator import compare_responses
from app.config import ComparisonConfig


def test_comparison_result_serializes_differences():
    result = compare_responses(200, {}, b'{"value":1}', 200, {}, b'{"value":2}', ComparisonConfig())
    serialized = result.as_dict()
    assert serialized["match"] is False
    assert serialized["differences"][0] == {"path": "$.body.value", "backend_a": 1, "backend_b": 2}
