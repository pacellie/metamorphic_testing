# enable type annotating the class itself,
# see https://stackoverflow.com/a/33533514/4306257
from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from metamorphic_test.transformation import MetamorphicTransformation

T1 = TypeVar('T1')
T2 = TypeVar('T2')
X = TypeVar('X')


class MetamorphicRelation(Generic[T1, T2], metaclass=ABCMeta):
    """A generalized metamorphic relation. It can assert a metamorphic relation."""
    @abstractmethod
    def relate_check(self, a: T1, b: T2) -> None:
        """Asserts that a and b are related."""
    
    def t_first(
        self,
        transformation: MetamorphicTransformation[X, T1]
    ) -> MetamorphicRelation[X, T2]:
        """
        Apply the transformation to the first result of the relation.
        Returns a new relation for that.
        """
        original = self

        class TFirst(MetamorphicRelation[X, T2]):
            def relate_check(self, a: X, b: T2) -> None:
                original.relate_check(transformation.transform(a), b)
        return TFirst()
    
    def t_second(
        self,
        transformation: MetamorphicTransformation[X, T2]
    ) -> MetamorphicRelation[T1, X]:
        """
        Apply the transformation to the second result of the relation.
        Returns a new relation for that.
        """
        original = self

        class TSecond(MetamorphicRelation[T1, X]):
            def relate_check(self, a: T1, b: X) -> None:
                original.relate_check(a, transformation.transform(b))
        return TSecond()
    
    def __and__(self, other_r: MetamorphicRelation[T1, T2]) -> MetamorphicRelation[T1, T2]:
        """
        Assert that both relations are related.
        """
        original = self

        class AndRelation(MetamorphicRelation[T1, T2]):
            def relate_check(self, a: T1, b: T2) -> None:
                original.relate_check(a, b)
                other_r.relate_check(a, b)
        return AndRelation()
    
    def __or__(self, other_r: MetamorphicRelation[T1, T2]) -> MetamorphicRelation[T1, T2]:
        """
        Assert that at least one relation is related.
        """
        original = self

        class OrRelation(MetamorphicRelation[T1, T2]):
            def relate_check(self, a: T1, b: T2) -> None:
                try:
                    original.relate_check(a, b)
                except AssertionError:
                    other_r.relate_check(a, b)
        return OrRelation()
    
    def not_(self) -> MetamorphicRelation[T1, T2]:
        """
        Assert that the relation is not related.
        """
        original = self

        class NotRelation(MetamorphicRelation[T1, T2]):
            def relate_check(self, a: T1, b: T2) -> None:
                try:
                    original.relate_check(a, b)
                except AssertionError:
                    pass
                else:
                    raise AssertionError("Expected not to be related, but was.")
        return NotRelation()


def relate(r: MetamorphicRelation):
    """
    A decorator that asserts that a metamorphic relation is respected.
    Usage: @relate(float_equal())
    """
    def decorator(fun):
        def related(anchor, transformed):
            r.relate_check(
                fun(anchor),
                fun(transformed)
            )
        return related
    return decorator
