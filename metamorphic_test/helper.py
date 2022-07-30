import inspect
import wrapt  # type: ignore
from typing import Callable

SignatureWrapper = Callable[[Callable], Callable]


def change_signature(adapt_func: Callable) -> SignatureWrapper:
    """
    Signature changing decorator.
    Changing from the original function signature to adapt_func function's.

    Parameters
    ----------
    adapt_func : Callable
        The function with the argument specification as a prototype will be sourced.

    Returns
    -------
    change : SignatureWrapper
        Returns a function that its signature has been dynamically
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
        if instance is None:
            return wrapped(*args, **kwargs)
        raise RuntimeError("'change_signature' decorator "
                           "should be applied to a class or a function.")

    return change
