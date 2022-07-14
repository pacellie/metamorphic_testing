import pytest

def approximately(x, y):
    return x == pytest.approx(y)


def equality(x, y):
    return x == y

def becomes_larger(x, y):
    return x < y

def becomes_smaller(x, y):
    return x > y

def or_(rel1, rel2):
    def or_impl(x, y):
        return rel1(x, y) or rel2(x, y)
    or_impl.__name__ = f'{rel1.__name__} or {rel2.__name__}'
    return or_impl
