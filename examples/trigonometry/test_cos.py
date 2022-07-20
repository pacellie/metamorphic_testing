import math
import pytest
from metamorphic_test import (
    transformation,
    metamorphic,
    system,
    randomized,
    fixed,
)
from metamorphic_test.generators import RandInt
from metamorphic_test.relations import approximately

A = metamorphic('A', relation=approximately)


@transformation(A)
@randomized('n', RandInt(1, 10))
@fixed('c', 0)
def shift(x, n, c):
    return x + 2 * n * math.pi + c


@pytest.mark.parametrize('x', range(-10, 10))
@system(name=A)
def test_cos(x):
    return math.cos(x)
