import inspect
import wrapt  # type: ignore


def argspec_factory(func):
    argspec = inspect.getfullargspec(func)
    return inspect.ArgSpec(argspec.args,
                           argspec.varargs,
                           argspec.varkw,
                           argspec.defaults)


def change_signature(adapt_func):
    @wrapt.decorator(adapter=argspec_factory(adapt_func))
    def change(wrapped, instance, args, kwargs):
        if instance is None:
            return wrapped(*args, **kwargs)
        raise RuntimeError("'change_signature' decorator "
                           "should be applied to a class or a function.")

    return change
