import math
import pytest
from metamorphic_test import (
    transformation,
    relation,
    metamorphic,
    system,
    randomized,
    randint,
    approximately
)

A = metamorphic('A', relation=approximately)
B = metamorphic('B')
C = metamorphic('C')
D = metamorphic('D')


# The order of randomized is not important, but the randomized decorators
# must be closest to the function definition. Randomized works with values, e.g.
# '0' or thunks, functions of the form lambda: value, e.g. 'randint(1, 10)'
@transformation(A)
@transformation(C, priority=1)
@randomized('n', randint(1, 10))
@randomized('c', 0)
def shift(x, n, c):
    return x + 2 * n * math.pi + c


@transformation(B)
@transformation(C, priority=0)
def negate(x):
    return -x


@relation(B)
@relation(C)
def approximately_negate(x, y):
    return approximately(-x, y)


@pytest.mark.parametrize('x', range(-1, 1))
@system(name=A)
def test_sin(x):
    return math.sin(x)
