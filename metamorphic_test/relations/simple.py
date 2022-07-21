from metamorphic_test.rel import A, B

def equality(x: A, y: A) -> bool:
    return x == y


def less_than(x: B, y: B) -> bool:
    return x < y


def greater_than(x: B, y: B) -> bool:
    return x > y