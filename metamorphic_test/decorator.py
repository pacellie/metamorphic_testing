import inspect
from collections import defaultdict
from functools import wraps

from .suite import Suite

suites: defaultdict = defaultdict(lambda: defaultdict(Suite))


def module(func):
    return inspect.getmodule(func)


def name(custom_name):
    def wrapper(transform):
        suites[module(transform)][transform.__name__].name = custom_name
        return transform

    return wrapper


def parametrized(arg, generator):
    def wrapper(transform):
        @wraps(transform)
        def parametrized_transform(*args, **kwargs):
            kwargs[arg] = generator() if callable(generator) else generator
            return transform(*args, **kwargs)

        return parametrized_transform

    return wrapper


def transformation(transform):
    suites[module(transform)][transform.__name__].transform = transform
    return transform


def relation(transform):
    def wrapper(relation):
        found_transform = False

        for suite in suites[module(relation)]:
            if suites[module(relation)][suite].transform == transform:
                suites[module(relation)][suite].relation = relation
                found_transform = True

        if not found_transform:
            raise TypeError(f"cannot find the corresponding transformation "
                            f"{transform.__name__} "
                            f"for the relation {relation.__name__}")

        return relation

    return wrapper


def metamorphic(sut):
    def execute(x):
        print(f"{suites=}")
        for suite in suites[module(sut)]:
            transform = suites[module(sut)][suite].transform
            relation = suites[module(sut)][suite].relation

            name = suites[module(sut)][suite].name \
                if suites[module(sut)][suite].name \
                else suite

            print(f"[running suite '{name}']"
                  f"\n\tinput: {x} "
                  f"\n\ttransform: {transform.__name__} "
                  f"\n\trelation: {relation.__name__}")

            assert relation(sut(x), sut(transform(x)))

    return execute
