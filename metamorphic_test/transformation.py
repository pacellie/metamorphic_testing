# enable type annotating the class itself,
# see https://stackoverflow.com/a/33533514/4306257
from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Generic, List, Literal, TypeVar, Any, Dict
# from functools import wraps


B = TypeVar('B')
F = TypeVar('F')
T = TypeVar('T')



class MetamorphicTransformation(Generic[F, T], metaclass=ABCMeta):
    """
    A generalized metamorphic transformation.
    It can transform a value (from type F to type T).
    """
    @abstractmethod
    def transform(self, anchor: F) -> T:
        """Transform the given value. Might take more parameters in implementations."""
    
    def chain(
        self,
        with_t: MetamorphicTransformation[B, F]
    ) -> MetamorphicTransformation[B, T]:
        """
        Chain two transformations.
        If T1 transforms F -> T and T2 transforms B -> F,
        then T1.chain(T2) transforms B -> T.
        If you want to pass parameters to the chained (inner) transformation,
        pass a list / dict as the parameter inner["args"] / inner["kwargs"].
        """
        original = self
        class ChainedTransformation(MetamorphicTransformation[B, T]):
            def transform(
                self,
                anchor: B,
                *args,
                inner: Dict[
                    (Literal['args'] | Literal['kwargs']),
                    (List | Dict[str, Any])] = None,
                **kwargs
            ) -> T:
                if inner is None:
                    inner = {}
                if not set(inner.keys()).issubset({'args', 'kwargs'}):
                    raise ValueError(
                        "inner can only contain keys 'args' and 'kwargs'")  # pragma: no cover
                inner_transformed = with_t.transform(anchor, *inner["args"], **inner["kwargs"])
                return original.transform(inner_transformed, *args, **kwargs)
        return ChainedTransformation()

    
    def __call__(
        self,
        with_t: MetamorphicTransformation[B, F]
    ) -> MetamorphicTransformation[B, T]:
        """
        Shorthand for chaining transformations.
        """
        return self.chain(with_t)
    

    def then(
        self,
        then_transform: MetamorphicTransformation[T, B]
    ) -> MetamorphicTransformation[F, B]:
        """
        Apply this transformation first,
        then then_transform. ("Reverse" of .chain).
        """
        return then_transform.chain(self)


def transform(t: MetamorphicTransformation[F, T]):
    """
    A decorator that transforms a value.
    Usage: @transform(shift(1))
    """
    def decorator(fun):
        # @wraps(fun)
        def transformed(anchor: F, *args, **kwargs) -> T:
            transformed = t.transform(anchor, *args, **kwargs)
            return fun(anchor, transformed)
        return transformed
    return decorator
