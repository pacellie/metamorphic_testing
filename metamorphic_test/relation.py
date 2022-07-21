from abc import ABCMeta, abstractmethod
from typing import TypeVar, Any, Callable


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __gt__(self, other: Any) -> bool:
        ...


A = TypeVar('A')
B = TypeVar('B', bound=Comparable)


Relation = Callable[[A, A], bool]
