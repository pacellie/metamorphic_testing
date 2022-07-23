from metamorphic_test.rel import A, B


def equality(x: A, y: A) -> bool:
    return x == y


def is_less_than(x: B, y: B) -> bool:
    return x < y


def is_greater_than(x: B, y: B) -> bool:
    return x < y

