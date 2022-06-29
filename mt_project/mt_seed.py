"""
Defines the strategy for generating `original_input`.
"""
from abc import ABC, abstractmethod
from typing import Union

import hypothesis.strategies as st
from hypothesis.strategies import SearchStrategy


class MtSeed(ABC):
    @abstractmethod
    def __init__(self) -> None:
        ...

    def __call__(self) -> SearchStrategy:
        return self.generate_seed()

    @abstractmethod
    def generate_seed(self) -> SearchStrategy:
        ...


class SineSeed(MtSeed):
    def __init__(self, *, min_value: Union[int, float], max_value: Union[int, float]) -> None:
        self.min_value: Union[int, float] = min_value
        self.max_value: Union[int, float] = max_value

    def generate_seed(self) -> SearchStrategy:
        return st.floats(min_value=self.min_value, max_value=self.max_value)
