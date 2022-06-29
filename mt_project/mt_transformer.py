"""
Defines the transformer method for transforming
from `original_input` into transformed_input.
"""
from math import pi
from abc import ABC, abstractmethod
from typing import Any

from hypothesis.strategies import SearchStrategy


class MtTransformer(ABC):
    def __init__(self, *, n: int = None):
        """
        `n` is used to define how many times
        the `original_input` applies to the transformer.
        """
        if n is None:
            n = 1  # default: transform 1 time

        self.n = n

    def __call__(self, original_input: SearchStrategy):
        return self.transformer(original_input)

    @staticmethod
    @abstractmethod
    def transformer(original_input: Any):
        ...


class SineTransformer(MtTransformer):
    @staticmethod
    def transformer(original_input: Any):
        return original_input + 2 * pi
