"""
Defines the relation between `original_output` and `transformed_output`.
"""
from __future__ import annotations
from typing import Any, Union
from pytest import approx
from abc import ABC, abstractmethod


class MtRelation(ABC):
    def __init__(self) -> None:
        """
        Stores the instance attributes for logging.
        """
        self.original_output: Any = None
        self.transformed_output: Any = None

    def __call__(self, **kwargs) -> Union[MtRelation, bool]:
        """
        Unpacks the `dict` values from `@given`.
        Applies the function to each input and gets the outputs for relation checking.
        """
        original_input, transformed_input, function = kwargs.values()
        self.original_output = function(original_input)
        self.transformed_output = function(transformed_input)
        return self.check_relation(self.original_output, self.transformed_output)

    @staticmethod
    @abstractmethod
    def check_relation(original_output: Any, transformed_output: Any) -> bool:
        ...


class FloatEqual(MtRelation):
    @staticmethod
    def check_relation(original_output: Any, transformed_output: Any) -> bool:
        return original_output == approx(transformed_output)
