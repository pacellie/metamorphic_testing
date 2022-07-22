from typing import TypeVar

from metamorphic_test.transform import A

A = TypeVar('A')

def identity(x: A) -> A:
    return x
