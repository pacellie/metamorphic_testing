from functools import wraps
import inspect
from .transforms import identity
from .relations import equality
from .suite import Suite

suite = Suite()


def metamorphic(name, *, transform=identity, relation=equality):
    suite.metamorphic(name, transform=transform, relation=relation)
    return name


def randomized(arg, generator):
    def wrapper(transform):
        @wraps(transform)
        def randomized_transform(*args, **kwargs):
            kwargs[arg] = generator() if callable(generator) else generator
            return transform(*args, **kwargs)

        return randomized_transform

    return wrapper


def transformation(name, *, priority=0):
    def wrapper(transform):
        suite.transformation(name, transform, priority=priority)
        return transform

    return wrapper


def relation(*names):
    def wrapper(relation):
        for name in names:
            suite.relation(name, relation)
        return relation

    return wrapper


def system(flag=None, *, name=None):
    def wrapper(test):
        def execute(*args):
            suite.execute(name, test, *args)

        # Creates a fake function that calls to the 'execute' function
        # with the exactly same signature as 'test'.
        sig = str(inspect.signature(test))
        func_def = f'lambda {sig[1:-1]}: execute{sig}'
        func = eval(func_def, {'execute': execute})
        return wraps(test)(func)

    if flag is None:
        return wrapper
    return wrapper(flag)
