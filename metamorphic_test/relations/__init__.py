"""
Contains some relations commonly used in metamorphic testing.

A relation is usually used to compare the results of the function to test
based on some anchor value provided as the parameter vs. a transformation
of that anchor.
"""

# import so that you can directly import from metamorphic_test.relations
from .approx_equal import ApproxEqual
from .equal import Equal
from .less_than import LessThan
from .greater_than import GreaterThan
from .swapped import Swapped


__all__ = [
    "ApproxEqual",
    "Equal",
    "LessThan",
    "GreaterThan",
    "Swapped",
]