import math
import pytest
from metamorphic_test import (
    transformation,
    relation,
    metamorphic,
    system,
    fixed,
    randomized,
)
from metamorphic_test.generators import RandInt
from metamorphic_test.relations import approximately


# Register a new metamorphic test by specifying it's name and optionally
# a transform and a relation.
A = metamorphic('A', relation=approximately)
B = metamorphic('B')
C = metamorphic('C')


# Register the 'shift' transform for test A with default priority 0 and test C
# with priority 1.
@transformation(A)
@transformation(C, priority=1)
# The order of randomized is not important, but the randomized decorators
# must be closest to the function definition. Randomized works with values, e.g.
# '0' or thunks, functions of the form lambda: value, e.g. 'randint(1, 10)'
@randomized('n', RandInt(1, 10))
@fixed('c', 0)
def shift(x: float, n: int, c: int) -> float:
    return x + 2 * n * math.pi + c


# Register the 'negate' transform for test B with default priority 0 and test C
# with priority 0.
@transformation(B)
@transformation(C, priority=0)
def negate(x: float) -> float:
    return -x


# Register the 'approximately_negate' relation for test B and test C.
@relation(B, C)
def approximately_negate(x: float, y: float) -> bool:
    return approximately(-x, y)


# Parametrize the input, in this case: -10, 9
@pytest.mark.parametrize('x', range(-10, 10))
# Mark this function as the system under test
@system()
def test_sin(x: float) -> float:
    return math.sin(x)
