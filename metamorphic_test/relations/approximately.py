import pytest

from metamorphic_test.rel import A


def approximately(x: A, y: A) -> bool:
    """
    Checks if the given arguments are approximately equal by delegating to
    pytest.approx.

    Parameters:
    -----------
    x : A
        The first generic argument.
    y : A
        The second generic argument.

    Returns:
    --------
    out : bool
        A boolean indicating if the two given arguments are approximately equal.

    Examples:
    ---------
    import math

    approximately(math.pi, 3.1315926536) # holds
    approximately(math.pi, 3.13) # does not hold
    """
    return x == pytest.approx(y)
