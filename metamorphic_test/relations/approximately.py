import pytest

from metamorphic_test.rel import A


def approximately(x: A, y: A) -> bool:
    return x == pytest.approx(y)

