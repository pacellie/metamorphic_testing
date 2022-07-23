import pytest
from typing import TypeVar, Tuple

from hypothesis import given
from hypothesis.strategies import floats
from metamorphic_test import (
    transformation,
    metamorphic,
    system,
)
from metamorphic_test.relations import equality

X = TypeVar('X')
Y = TypeVar('Y')


A = metamorphic('A', relation=equality)


@transformation(A)
def swap(x: X, y: Y) -> Tuple[Y, X]:
    return y, x


@given(floats(allow_nan=False, allow_infinity=False),
       floats(allow_nan=False, allow_infinity=False))
@system(A)
def test_add_given(x: float, y: float) -> float:
    return x + y


@pytest.mark.parametrize('x', [0, 1])
@pytest.mark.parametrize('y', [2, 3])
@system(A)
def test_add_pytest(x: int, y: int) -> int:
    return x + y
