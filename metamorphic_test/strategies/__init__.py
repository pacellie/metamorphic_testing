"""Contains some additional useful hypothesis strategies for metamorphic testing."""

from .floats_without_weird import floats_without_weird
from .inner import inner


__all__ = [
    "floats_without_weird",
    "inner",
]