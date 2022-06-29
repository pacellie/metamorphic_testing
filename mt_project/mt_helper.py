"""
Helper functions for manipulating the values that get from `@mt_given`.
"""
from typing import Callable, Type
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.strategies import SearchStrategy

import mt_transformer as mt
import mt_function as mf
import mt_relation as mr
import mt_seed as ms


def _poor_logging(relation_instance: mr.MtRelation) -> None:
    """
    Temporary logging for having a look at the test outputs.
    Since logging by `print` is not wanted, this should be changed later.
    """
    print(
        f"{relation_instance.original_output=!r}, "
        f"{relation_instance.transformed_output=!r}"
    )


def _get_input_seeds(seed: ms.MtSeed, transformer: mt.MtTransformer) -> tuple[SearchStrategy, SearchStrategy]:
    """
    Returns a tuple of original input and transformed input.
    """
    sample: SearchStrategy = seed()
    original_input: SearchStrategy = st.shared(sample, key="same")
    transformed_input: SearchStrategy = st.shared(sample, key="same")

    # The `transformed_input` is generated based on the same value as `original_input`,
    # and mapped to the `transformer` function for `n` times,
    # where `n` is given when instantiating the `MtTransformer` class.
    for i in range(transformer.n):
        transformed_input = transformed_input.map(transformer)

    return original_input, transformed_input


def mt_given(
        *,
        seed: ms.MtSeed,
        transformer: mt.MtTransformer,
        function: Type[mf.MtFunction],
        relation: Type[mr.MtRelation]
) -> Callable:
    """
    A decorator built on top of `@given` to accept the keyword-only arguments.
    Arranges the arguments, reformat them to a `dict`,
    and unpack the `dict` into the parameters of `wrapper` function.
    """

    def inner_given(func: Callable) -> Callable:
        original_input, transformed_input = _get_input_seeds(
            seed,
            transformer,
        )

        @given(**{
            "original_input": original_input,
            "transformed_input": transformed_input,
            # Instantiates the `function` and `relation` classes,
            # which are inherited from `MtFunction` and `MtRelation` respectively.
            "function": st.sampled_from([function()]),
            "relation": st.sampled_from([_relation_instance := relation()]),
        })
        def wrapper(*args, **kwargs) -> None:
            try:
                func(*args, **kwargs)
            # If the test fails, catch the `AssertionError` and do poor logging.
            except AssertionError:
                raise AssertionError(_poor_logging(_relation_instance))

        return wrapper

    return inner_given
