import math

from hypothesis import given
import hypothesis.strategies as st

from metamorphic_test import transform, relate
from metamorphic_test.relations import float_equal
from metamorphic_test.transformations import shift


@given(
    anchor=st.floats(
        min_value=-10, max_value=10,
        allow_infinity=False, allow_nan=False
    ),
    multiple=st.integers(
        min_value=-10, 
        max_value=10
    )
)
@transform(shift(2 * math.pi))
@relate(float_equal())
def test_sin(v):
    return math.sin(v)
