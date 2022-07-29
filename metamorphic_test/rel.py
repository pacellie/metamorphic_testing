from abc import ABCMeta, abstractmethod
from typing import TypeVar, Any, Callable


class Comparable(metaclass=ABCMeta):
    """
    This abstract base class used to mark that any type implementing this
    class must support the common comparison operators.

    It is used for exclusively for typing.
    """
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __le__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __gt__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __ge__(self, other: Any) -> bool:
        ...


"""Common type variable for unconstrained relations."""
A = TypeVar('A')
# any type which instantiates the type variable 'B' must support the common
# comparison operators defined in the 'Comparable' class
"""
Common type variable for relations which contrain the type to support python's
usual comparison operators. Also see the 'Comparable' ABC.
"""
B = TypeVar('B', bound=Comparable)


"""The general type of an un-constrained relation."""
Relation = Callable[[A, A], bool]
