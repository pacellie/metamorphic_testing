from collections import defaultdict
from functools import wraps, partial

from .suite import Suite

suites: defaultdict = defaultdict(lambda: defaultdict(Suite))


def name(custom_name):
    def wrapper(transform):
        suites[transform.__module__][transform.__name__].name = custom_name
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
    suites[transform.__module__][transform.__name__].transform = transform
    return transform


def relation(*transforms):  # transformation functions
    def wrapper(relation):
        for transform in transforms:
            found_transform = False

            for suite in suites[relation.__module__]:
                if suites[relation.__module__][suite].transform == transform:
                    suites[relation.__module__][suite].relation = relation
                    found_transform = True

            if not found_transform:
                raise TypeError(f"cannot find the corresponding transformation "
                                f"{transform.__name__} "
                                f"for the relation {relation.__name__}")

        return relation

    return wrapper


def metamorphic(test=None, *, relation=None):
    if test is None:  # metamorphic was called with arguments
        return partial(metamorphic, relation=relation)

    def execute(x):
        print(f"{suites=}")
        for suite in suites[test.__module__]:
            transform = suites[test.__module__][suite].transform
            relation = suites[test.__module__][suite].relation

            name = suites[test.__module__][suite].name \
                if suites[test.__module__][suite].name \
                else suite

            print(f"[running suite '{name}']"
                  f"\n\tinput: {x} "
                  f"\n\ttransform: {transform.__name__} "
                  f"\n\trelation: {relation.__name__}")

            assert relation(test(x), test(transform(x)))

    return execute
