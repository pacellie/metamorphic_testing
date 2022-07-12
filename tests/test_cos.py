import math
import pytest
from metamorphic_test import (
    transformation,
    metamorphic,
    system,
    randomized,
    randint,
    approximately
)

A = metamorphic('A', relation=approximately)


@transformation(A)
@randomized('n', randint(1, 10))
@randomized('c', 0)
def shift(x, n, c):
    return x + 2 * n * math.pi + c



@pytest.mark.parametrize('x', range(-1, 1))
@system
def test(x):
    return math.cos(x)
