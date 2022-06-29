from typing import Any
from metamorphic_test.relation import MetamorphicRelation


class Equal(MetamorphicRelation[Any, Any]):
    """A metamorphic relation compares using equality."""
    def relate_check(self, a: Any, b: Any) -> None:
        assert a == b