import pytest


def approximately(x, y):
    return x == pytest.approx(y)


def equality(x, y):
    return x == y
