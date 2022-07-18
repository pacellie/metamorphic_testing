import pytest
from hypothesis import given
from hypothesis.strategies import floats
from metamorphic_test import (
    transformation,
    metamorphic,
    system,    
)
from metamorphic_test.relations import equality


A = metamorphic('A', relation=equality)


@transformation(A)
def swap(x, y):
    return y, x


@given(floats(allow_nan=False, allow_infinity=False),
       floats(allow_nan=False, allow_infinity=False))
@system
def test_add_given(x, y):
    return x + y


@pytest.mark.parametrize('x', [0, 1])
@pytest.mark.parametrize('y', [2, 3])
@system
def test_add_pytest(x, y):
    return x + y
