from abc import ABCMeta, abstractmethod
from typing import TypeVar, Any, Callable


class Comparable(metaclass=ABCMeta):
    """Class to mark that any type implementing that class must support
    the common comparison operators."""
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
# any type which instantiates the type variable 'B' must support the common
# comparison operators defined in the 'Comparable' class
B = TypeVar('B', bound=Comparable)


Relation = Callable[[A, A], bool]
