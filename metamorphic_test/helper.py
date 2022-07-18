import inspect
import wrapt  # type: ignore


def change_signature(adapt_func):
    fullargspec = inspect.getfullargspec(adapt_func)
    fullargspec.args.insert(0, 'name')

    @wrapt.decorator(adapter=fullargspec)
    def change(wrapped, instance, args, kwargs):
        if instance is None:
            return wrapped(*args, **kwargs)
        raise RuntimeError("'change_signature' decorator "
                           "should be applied to a class or a function.")

    return change
