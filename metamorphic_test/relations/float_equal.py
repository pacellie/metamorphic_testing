from metamorphic_test.relation import MetamorphicRelation
from pytest import approx


def float_equal() -> MetamorphicRelation[float]:
    """A metamorphic relation that asserts that two floats are roughly equal."""
    class FloatEqual(MetamorphicRelation[float]):
        def relate_check(self, a: float, b: float) -> None:
            assert a == approx(b)
    return FloatEqual()