"""
Defines the strategy for generating `original_input`.
"""
from abc import ABC, abstractmethod
from typing import Union

import hypothesis.strategies as st


class MtSeed(ABC):
    @abstractmethod
    def __init__(self):
        ...

    def __call__(self):
        return self.generate_seed()

    @abstractmethod
    def generate_seed(self):
        ...


class SineSeed(MtSeed):
    def __init__(self, *, min_value: Union[int, float], max_value: Union[int, float]):
        self.min_value: Union[int, float] = min_value
        self.max_value: Union[int, float] = max_value

    def generate_seed(self):
        return st.floats(min_value=self.min_value, max_value=self.max_value)
