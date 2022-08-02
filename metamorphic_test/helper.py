import inspect
import wrapt  # type: ignore
from typing import Callable

SignatureWrapper = Callable[[Callable], Callable]


def change_signature(adapt_func: Callable) -> SignatureWrapper:
    """
    Signature changing decorator.
    Change the original function's signature to adapt_func's.

    Parameters
    ----------
    adapt_func : Callable
        The function which will be used as source of the argument specification.

    Returns
    -------
    change : SignatureWrapper
        Returns a function whose signature has been dynamically
        changed with annotations based on the adapt_func function.

    Examples
    --------
    def prototype(arg1, arg2): pass

    @change_signature(prototype)
    def function(input):
        ...
    """
    fullargspec = inspect.getfullargspec(adapt_func)
    fullargspec.args.insert(0, 'name')

    @wrapt.decorator(adapter=fullargspec)
    def change(wrapped, instance, args, kwargs):
        def _raise_runtime_err(applied_type):
            raise RuntimeError(f"'change_signature' decorator should not"
                               f" be applied to a {applied_type}.")

        if instance is None:
            if not inspect.isclass(wrapped):
                # Decorator was applied to a function or staticmethod.
                return wrapped(*args, **kwargs)
            # Decorator was applied to a class.
            return _raise_runtime_err('class')

        if inspect.isclass(instance):
            # Decorator was applied to a classmethod.
            return _raise_runtime_err('classmethod')

        # Decorator was applied to an instancemethod.
        return _raise_runtime_err('instancemethod')

    return change
