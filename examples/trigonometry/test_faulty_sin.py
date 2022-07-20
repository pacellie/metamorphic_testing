import math
import pytest
from metamorphic_test import (
    transformation,
    relation,
    metamorphic,
    system,
    randomized,
)
from metamorphic_test.generators import RandInt
from metamorphic_test.relations import approximately


class MathLibrary():
    __PI = 3.14159265358979323846
    __PRECISION = 15

    @staticmethod
    def sin(x):
        x %= 2 * MathLibrary.__PI

        if x < 0:
            return -MathLibrary.sin(-x)

        if x > MathLibrary.__PI:
            return -MathLibrary.sin(x - MathLibrary.__PI)

        assert x >= 0
        assert x <= MathLibrary.__PI

        for i in range(1, MathLibrary.__PRECISION + 1):
            if i % 2 == 0:
                x += math.pow(x, 2 * i + 1) / MathLibrary.factorial(2 * i + 1)
            else:
                x -= math.pow(x, 2 * i + 1) / MathLibrary.factorial(2 * i + 1)

        return x

    @staticmethod
    def factorial(n):
        fact = 1
        for i in range(1, n + 1):
            fact = fact * i
        return fact


test_two_pi = metamorphic('Plus 2 π', relation=approximately)
test_negate_x = metamorphic('sin(-x)')
test_plus_pi = metamorphic('Plus 1 π')
test_pi_minus_x = metamorphic('sin(π-x)', relation=approximately)


@transformation(test_two_pi)
@randomized('n', RandInt(0, 10))
def two_pi_shift(x, n):
    return x + 2 * n * math.pi


@transformation(test_negate_x)
def negate(x):
    return -x


@transformation(test_plus_pi)
def pi_shift(x):
    return x + math.pi


@transformation(test_pi_minus_x)
def pi_shift_minus(x):
    return math.pi - x


@relation(test_negate_x, test_plus_pi)
def approximately_negate(x, y):
    return approximately(-x, y)


@pytest.mark.skip
@pytest.mark.parametrize('x', range(-10, 10))
# TODO: make this work again with multiple tests for one system
@system(name=test_two_pi) # test_negate_x, test_plus_pi, test_pi_minus_x
def test(x):
    return MathLibrary.sin(x)
