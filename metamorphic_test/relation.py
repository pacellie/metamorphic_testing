from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class MetamorphicRelation(Generic[T], metaclass=ABCMeta):
    """A generalized metamorphic relation. It can assert a metamorphic relation."""
    @abstractmethod
    def relate_check(self, a: T, b: T) -> None:
        """Asserts that a and b are related."""
        ...


def relate(r: MetamorphicRelation):
    """
    A decorator that asserts that a metamorphic relation is respected.
    Usage: @relate(float_equal())
    """
    def decorator(fun):
        def inner(anchor, transformed):
            r.relate_check(
                fun(anchor),
                fun(transformed)
            )
        return inner
    return decorator
