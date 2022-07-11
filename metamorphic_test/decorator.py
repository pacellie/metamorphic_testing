from collections import defaultdict
from functools import wraps, partial
from .suite import Suite
import inspect

suites: defaultdict = defaultdict(lambda: defaultdict(Suite))

def metamorphic(metamorphic_name):
    suite = Suite(name=metamorphic_name)
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    print(module)
    suites[module][metamorphic_name] = suite
    return metamorphic_name


# def name(custom_name):
#     def wrapper(transform):
#         suites[transform.__module__][transform.__name__].name = custom_name
#         return transform
#
#     return wrapper


def randomized(arg, generator):
    def wrapper(transform):
        @wraps(transform)
        def parametrized_transform(*args, **kwargs):
            kwargs[arg] = generator() if callable(generator) else generator
            return transform(*args, **kwargs)

        return parametrized_transform

    return wrapper


def transformation(metamorphic_name):
    def wrapper(transform):
        suites[transform.__module__][metamorphic_name].transform = transform
        return transform
    return wrapper



def relation(metamorphic_name):
    def wrapper(relation):
        suites[relation.__module__][metamorphic_name].relation = relation
        return relation
    return wrapper


def system(test):
    print("kguiiutr")
    def execute(x):
        for suite in suites[test.__module__]:
            transform_ = suites[test.__module__][suite].transform
            relation_ = suites[test.__module__][suite].relation

            if relation and relation != relation_:
                continue

            name = suites[test.__module__][suite].name \
                if suites[test.__module__][suite].name \
                else suite

            print(f"[running suite '{name}']"
                  f"\n\tinput: {x} "
                  f"\n\ttransform: {transform_.__name__} "
                  f"\n\trelation: {relation_.__name__}")

            assert relation_(test(x), test(transform_(x)))

    return execute
