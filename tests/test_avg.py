import pytest
from metamorphic_test import (
    transformation,
    metamorphic,
    system,
    equality
)

A = metamorphic('A', relation=equality)


@transformation(A)
def swap(a, b, c):
    return c, b, a


@pytest.mark.parametrize('a', [0, 1])
@pytest.mark.parametrize('b', [2, 3])
@pytest.mark.parametrize('c', [4, 5])
@system
def test_avg(a, b, c):
    return (a + b + c)/3
