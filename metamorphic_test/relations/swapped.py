from typing import Any
from metamorphic_test.relation import MetamorphicRelation


class Swapped(MetamorphicRelation[Any, Any]):
    """A metamorphic relation based on another relation with the parameters swapped."""
    def __init__(self, relation: MetamorphicRelation[Any, Any]):
        self.relation = relation

    def relate_check(self, a: Any, b: Any) -> None:
        self.relation.relate_check(b, a)
