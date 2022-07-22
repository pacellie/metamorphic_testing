import pytest


def approximately(x, y):
    return x == pytest.approx(y)
