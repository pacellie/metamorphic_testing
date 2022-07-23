import pytest
from typing import TypeVar, Tuple

from metamorphic_test import (
    transformation,
    metamorphic,
    system,
)
from metamorphic_test.relations import equality

X = TypeVar('X')
Y = TypeVar('Y')
Z = TypeVar('Z')


A = metamorphic('A', relation=equality)


@transformation(A)
def swap(a: X, b: Y, c: Z) -> Tuple[Z, Y, X]:
    return c, b, a


@pytest.mark.parametrize('a', [0, 1])
@pytest.mark.parametrize('b', [2, 3])
@pytest.mark.parametrize('c', [4, 5])
@system(A)
def test_avg(a: int, b: int, c: int) -> float:
    return (a + b + c)/3
