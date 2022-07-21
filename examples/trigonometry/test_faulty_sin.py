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
    def sin(x: float) -> float:
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
    def factorial(n: int) -> int:
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
def two_pi_shift(x: float, n: int) -> float:
    return x + 2 * n * math.pi


@transformation(test_negate_x)
def negate(x: float) -> float:
    return -x


@transformation(test_plus_pi)
def pi_shift(x: float) -> float:
    return x + math.pi


@transformation(test_pi_minus_x)
def pi_shift_minus(x: float) -> float:
    return math.pi - x


@relation(test_negate_x, test_plus_pi)
def approximately_negate(x: float, y: float) -> bool:
    return approximately(-x, y)


# @pytest.mark.skip
@pytest.mark.parametrize('x', range(-10, 10))
@system(test_two_pi, test_negate_x, test_plus_pi, test_pi_minus_x)
def test(x: float) -> float:
    return MathLibrary.sin(x)
