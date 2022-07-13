from collections import defaultdict
from functools import wraps, partial
from .metamorphic import MetamorphicTest
import inspect
from .transforms import identity
from .relations import equality

suites: defaultdict = defaultdict(lambda: defaultdict(MetamorphicTest))


def metamorphic(name, *, transform=identity, relation=equality):
    suite = MetamorphicTest(name=name, transforms=[(transform, 0)], relation=relation)
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    suites[module.__name__][name] = suite
    return name


def randomized(arg, generator):
    def wrapper(transform):
        @wraps(transform)
        def parametrized_transform(*args, **kwargs):
            kwargs[arg] = generator() if callable(generator) else generator
            return transform(*args, **kwargs)

        return parametrized_transform

    return wrapper


def transformation(name, *, priority=0):
    def wrapper(transform):
        suites[transform.__module__][name].transforms.append((transform, priority))
        return transform

    return wrapper


def relation(*names):
    def wrapper(relation):
        for name in names:
            suites[relation.__module__][name].relation = relation
        return relation

    return wrapper


def system(flag=None, *, name=None):
    def wrapper(test):
        def execute(*args):
            for suite in suites[test.__module__]:
                if name and suite != name:
                    continue

                suites[test.__module__][suite].execute(test, *args)

        # Creates a fake function that calls to the 'execute' function
        # with the exactly same signature as 'test'.
        sig = str(inspect.signature(test))
        func_def = f'lambda {sig[1:-1]}: execute{sig}'
        func = eval(func_def, {'execute': execute})
        return wraps(test)(func)

    if flag is None:
        return wrapper
    return wrapper(flag)
