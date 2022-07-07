import math
import pytest
import hypothesis.strategies as st
from metamorphic_test import transformation, relation, sut, name, parametrized


@transformation
@name("Plus 2 pi")
@parametrized("n", [1, 2, 3])  # Note: this is out of order
@parametrized("c", [0])
def plus_two_pi(x, n, c):
    return x + 2 * n * math.pi + c


@relation(plus_two_pi)
def check_relation(first, second):
    return first == pytest.approx(second)


@transformation
def point_mirror(x):
    return -x


@relation(point_mirror)
def check_relation(first, second):
    return first == -second


@sut(x=st.floats(-5, 5))
def test_sin(x):
    return math.sin(x)
