import math
import pytest
from metamorphic_test import transformation, relation, metamorphic, name, parametrized, randint


# The order of parametrized is not important, but the parametrized decorators
# must be closest to the function definition. Parametrized works with values, e.g.
# '0' or thunks, functions of the form lambda: value, e.g. 'randint(1, 10)'
@transformation
@name('custom suite name')
@parametrized('n', randint(1, 10))
@parametrized('c', 0)
def shift(x, n, c):
    return x + 2 * n * math.pi + c


@transformation
def do_nothing(x):
    return x


@relation(shift, do_nothing)
def approximately(x, y):
    return x == pytest.approx(y)


@transformation
def negate(x):
    return -x


@relation(negate)
def approximately_negate(x, y):
    return -x == pytest.approx(y)


@pytest.mark.parametrize('x', range(-10, 10))
@metamorphic(relation=approximately_negate)
def test(x):
    return math.sin(x)
