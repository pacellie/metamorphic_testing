from collections import defaultdict
from .suite import Suite


suites: defaultdict = defaultdict(Suite)


def name(custom_name):
    def wrapper(transform):
        suites[transform.__name__].name = custom_name
        return transform
    return wrapper


def parametrized(arg, generator):
    def wrapper(transform):
        def parametrized_transform(*args, **kwargs):
            kwargs[arg] = generator() if callable(generator) else generator
            return transform(*args, **kwargs)
        return parametrized_transform
    return wrapper


def transformation(transform):
    suites[transform.__name__].transform = transform
    return transform


def relation(transform):
    def wrapper(relation):
        found_transform = False

        for suite in suites:
            if suites[suite].transform == transform:
                suites[suite].relation = relation
                found_transform = True

        if not found_transform:
            raise TypeError(f"cannot find the corresponding transformation "
                            f"{transform.__name__} "
                            f"for the relation {relation.__name__}")

        return relation
    return wrapper


def metamorphic(sut):
    def execute(x):
        for suite in suites:
            transform = suites[suite].transform
            relation = suites[suite].relation

            name = suites[suite].name if suites[suite].name else suite
            print(f"[running suite '{name}']"
                  f"\n\tinput: {x} "
                  f"\n\ttransform: {transform.__name__} "
                  f"\n\trelation: {relation.__name__}")

            assert relation(sut(x), sut(transform(x)))
    return execute
