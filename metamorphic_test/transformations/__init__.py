"""
Contains some transformations commonly used in metamorphic testing.

A transformation is usually meant to be applied before the function to test.
"""
from .negate import Negate
from .shift import Shift


__all__ = [
    "Negate",
    "Shift",
]