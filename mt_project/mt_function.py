"""
Defines the function that we want to do the metamorphic test.
"""
from math import sin
from abc import ABC, abstractmethod
from typing import Any


class MtFunction(ABC):
    def __call__(self, given_input: Any):
        return self.function(given_input)

    @staticmethod
    @abstractmethod
    def function(given_input: Any):
        ...


class SineFunction(MtFunction):
    @staticmethod
    def function(given_input: Any):
        return sin(given_input)
