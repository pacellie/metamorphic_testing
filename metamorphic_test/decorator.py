from functools import wraps
from .transforms import identity
from .relations import equality
from .suite import Suite
from .helper import change_signature

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
        @change_signature(test)
        def execute(*args, **kwargs):
            if kwargs:  # to be compatible with both given and pytest
                args = tuple(kwargs.values())
            suite.execute(name, test, *args)

        return execute

    if flag is None:
        return wrapper
    return wrapper(flag)
