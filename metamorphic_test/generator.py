from abc import ABCMeta
from typing import TypeVar, Generic

A = TypeVar('A')


class MetamorphicGenerator(Generic[A], metaclass=ABCMeta):
    def generate(self) -> A:
        ...
