from abc import ABCMeta, abstractmethod
from typing import TypeVar, Any, Callable


class Comparable(metaclass=ABCMeta):
    """
    This abstract base class is used to mark that any type implementing this
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


A = TypeVar('A')
"""Common type variable for unconstrained relations."""


B = TypeVar('B', bound=Comparable)
"""
Common type variable for relations which contrain the type to support python's
usual comparison operators. Also see the 'Comparable' ABC.
"""


Relation = Callable[[A, A], bool]
"""The general type of an un-constrained relation."""
