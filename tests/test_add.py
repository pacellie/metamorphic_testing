from hypothesis import given
from hypothesis.strategies import tuples, floats
from metamorphic_test import (
    transformation,
    metamorphic,
    system,
    equality
)

A = metamorphic('A', relation=equality)


@transformation(A)
def swap(xy):
    return (xy[1], xy[0])


@given(tuples(floats(allow_nan=False, allow_infinity=False),
              floats(allow_nan=False, allow_infinity=False)))
@system
def test(xy):
    return xy[0] + xy[1]
