import inspect
import wrapt  # type: ignore


def change_signature(adapt_func):
    fullargspec = inspect.getfullargspec(adapt_func)
    fullargspec.args.insert(0, 'name')

    @wrapt.decorator(adapter=fullargspec)
    def change(wrapped, instance, args, kwargs):
        if instance is None:
            if inspect.isclass(wrapped):
                # Decorator was applied to a class.
                raise RuntimeError("'change_signature' decorator should not "
                                   "be applied to a class.")
            else:
                # Decorator was applied to a function or staticmethod.
                return wrapped(*args, **kwargs)
        else:
            if inspect.isclass(instance):
                # Decorator was applied to a classmethod.
                raise RuntimeError("'change_signature' decorator should not "
                                   "be applied to a classmethod.")
            else:
                # Decorator was applied to an instancemethod.
                raise RuntimeError("'change_signature' decorator should not "
                                   "be applied to an instancemethod.")

    return change
