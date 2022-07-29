from metamorphic_test.rel import A, B


def equality(x: A, y: A) -> bool:
    """
    Checks if the given arguments are exactly equal by delegating to
    python's built-in equality operator.

    Parameters:
    -----------
    x : A
        The first generic argument.
    y : A
        The second generic argument.

    Returns:
    --------
    out : bool
        A boolean indicating if the two given arguments are exactly equal.

    Examples:
    ---------
    equality(1, 1) # holds
    equaltiy(1, 2) # does not hold
    """
    return x == y


def is_less_than(x: B, y: B) -> bool:
    """
    Checks if the first argument is strictly less than the second argument by
    delegating to python's built-in '<'-operator.

    Parameters:
    -----------
    x : A
        The first generic argument.
    y : A
        The second generic argument.

    Returns:
    --------
    out : bool
        A boolean indicating if the first argument is strictly less than the
        second argument.

    Examples:
    ---------
    is_less_than(1, 2) # holds
    is_less_than(2, 1) # does not hold
    """
    return x < y


def is_greater_than(x: B, y: B) -> bool:
    """
    Checks if the first argument is strictly greater than the second argument by
    delegating to python's built-in 'gt'-operator.

    Parameters:
    -----------
    x : A
        The first generic argument.
    y : A
        The second generic argument.

    Returns:
    --------
    out : bool
        A boolean indicating if the first argument is strictly greater than the
        second argument.

    Examples:
    ---------
    is_greater_than(2, 1) # holds
    is_greater_than(1, 2) # does not hold
    """
    return x > y
