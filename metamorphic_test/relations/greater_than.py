from typing import Any
from metamorphic_test.relation import MetamorphicRelation


class GreaterThan(MetamorphicRelation[Any, Any]):
    """A metamorphic relation for >."""
    def relate_check(self, a: Any, b: Any) -> None:
        assert a > b