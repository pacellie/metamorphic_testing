"""
Tests sine example using the modules defined in mt_* files.
"""
from typing import Union

import mt_transformer as mt
import mt_function as mf
import mt_relation as mr
import mt_seed as ms
import mt_helper as mh


@mh.mt_given(
    seed=ms.SineSeed(min_value=-10, max_value=10),
    # n: transform 3 times, e.g. x+(2*pi)*n, default n=1
    transformer=mt.SineTransformer(n=3),
    function=mf.SineFunction,
    relation=mr.FloatEqual,
)
def test_sine(
        relation: mr.MtRelation,
        **kwargs: dict[str, Union[ms.SineSeed, mt.SineTransformer, mf.SineFunction]]
) -> None:
    """
    Sine example which tests by pytest.
    Configures with the defined arguments that pass to `@mt_given`.
    The test function signature and assertion remain the same for different tests.
    """
    assert relation(**kwargs)
