import math

from hypothesis import given
import hypothesis.strategies as st

from metamorphic_test import transform, relate
from metamorphic_test.relations import ApproxEqual, Equal, LessThan, GreaterThan, Swapped
from metamorphic_test.strategies import inner
from metamorphic_test.transformations import Negate, Shift
import metamorphic_test.strategies as mst


# sin(x) = sin(x + 2\pi * n)
@given(
    anchor=mst.floats_without_weird(-10, 10),
    multiple=st.integers(-10, 10)
)
@transform(Shift(2 * math.pi))
@relate(ApproxEqual())
def test_sin_shift(v):
    return math.sin(v)


# -sin(x) = sin(-x)
@given(
    anchor=mst.floats_without_weird(-10, 10)
)
@transform(Negate())
@relate(ApproxEqual().t_first(Negate()))
def test_sin_symmetry(v):
    return math.sin(v)


# -sin(x + 2\pi * n) = sin(-(x + 2\pi * n))
# using .then
@given(
    anchor=mst.floats_without_weird(-10, 10),
    inner=inner(multiple=st.integers(-10, 10))
)
@transform(Shift(2 * math.pi).then(Negate()))
@relate(ApproxEqual().t_first(Negate()))
def test_sin_shift_and_symmetry_then(v):
    return math.sin(v)


# -sin(x + 2\pi * n) = sin(-(x + 2\pi * n))
# using .chain
@given(
    anchor=mst.floats_without_weird(-10, 10),
    inner=inner(multiple=st.integers(-10, 10))
)
@transform(Negate().chain(Shift(2 * math.pi)))
@relate(ApproxEqual().t_first(Negate()))
def test_sin_shift_and_symmetry_chain(v):
    return math.sin(v)


# -sin(x + 2\pi * n) = sin(-(x + 2\pi * n))
# using __call__ magic
@given(
    anchor=mst.floats_without_weird(-10, 10),
    inner=inner(multiple=st.integers(-10, 10))
)
@transform(Negate()(Shift(2 * math.pi)))
@relate(ApproxEqual().t_first(Negate()))
def test_sin_shift_and_symmetry_call(v):
    return math.sin(v)


# sin(x) != sin(x + \pi)
# and, for some reason (just as a demo)
# sin(x + \pi) != sin(x)
@given(
    anchor=mst.floats_without_weird(-10, 10)
)
@transform(Shift(math.pi))
@relate(
    Equal().not_() & Swapped(Equal()).not_()
)
def test_sin_one_pi_shifted(v):
    return math.sin(v)


# sin(x) < sin(x + \pi)
# or sin(x) > sin(x + \pi)
@given(
    anchor=mst.floats_without_weird(-10, 10)
)
@transform(Shift(math.pi))
@relate(
    GreaterThan() | LessThan()
)
def test_sin_one_pi_shifted_gl(v):
    return math.sin(v)


# A bit weird, but should be true:
# sin(k) > sin(k + \pi) + 0.5 for 0.6 < k < 2.5
@given(
    anchor=mst.floats_without_weird(0.6, 2.55)
)
@transform(Shift(math.pi))
@relate(
    GreaterThan().t_second(Shift(+ 0.5))
)
def test_sin_two_pi_shifted_gl(v):
    return math.sin(v)
