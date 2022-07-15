import inspect
import wrapt  # type: ignore


def change_signature(adapt_func):
    @wrapt.decorator(adapter=inspect.getfullargspec(adapt_func))
    def change(wrapped, instance, args, kwargs):
        if instance is None:
            return wrapped(*args, **kwargs)
        raise RuntimeError("'change_signature' decorator "
                           "should be applied to a class or a function.")

    return change
