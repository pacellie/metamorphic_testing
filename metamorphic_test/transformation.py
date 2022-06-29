from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from functools import wraps


T = TypeVar('T')


class MetamorphicTransformation(Generic[T], metaclass=ABCMeta):
    """A generalized metamorphic transformation. It can transform a value."""
    @abstractmethod
    def transform(self, anchor: T, *args, **kwargs) -> T:
        ...


def transform(t: MetamorphicTransformation):
    """
    A decorator that transforms a value.
    Usage: @transform(shift(1))
    """
    def decorator(fun):
        @wraps(fun)
        def inner(anchor, *args, **kwargs):
            transformed = t.transform(anchor, *args, **kwargs)
            return fun(anchor, transformed)
        return inner
    return decorator
