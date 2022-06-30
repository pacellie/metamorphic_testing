from typing import Any
from metamorphic_test.relation import MetamorphicRelation
from pytest import approx


class ApproxEqual(MetamorphicRelation[Any, Any]):
    """A metamorphic relation compares using pytest.approx."""
    def relate_check(self, a: Any, b: Any) -> None:
        assert a == approx(b)
