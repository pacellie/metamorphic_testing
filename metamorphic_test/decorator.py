from collections import defaultdict
from functools import wraps
from hypothesis import given
import hypothesis.strategies as st
from .suite import Suite

suite: defaultdict = defaultdict(Suite)


def name(custom_name):
    def deco_name(func):
        suite[func.__name__].name = custom_name
        return func

    return deco_name


def parametrized(*args):
    def deco_parametrized(func):
        suite[func.__name__].parametrized.append(args)
        return func

    return deco_parametrized


def transformation(func):
    suite[func.__name__].transformation = func
    return func


def relation(transformation_function):
    def deco_relation(func):
        found_mapping_transformation = False
        for s in suite:
            if suite[s].transformation == transformation_function:
                suite[s].relation = func
                found_mapping_transformation = True
        if not found_mapping_transformation:
            raise TypeError(f"cannot find the corresponding transformation function "
                            f"{transformation_function.__name__} "
                            f"for the relation function {func.__name__}")

        @wraps(func)
        def wrapper_relation(*args, **kwargs):  # first, second args of relation
            return func(*args, **kwargs)

        return wrapper_relation

    return deco_relation


def suite_key(func, key, anchor, **para_dict):
    def execute(**kwargs):
        first = kwargs[next(iter(kwargs))]  # retrieve the first arg
        test_function = func
        transformation_function = suite[key].transformation
        relation_function = suite[key].relation
        original_output = test_function(first)
        transformed_output = test_function(transformation_function(**kwargs))
        result = relation_function(original_output, transformed_output)
        assert result

    return given(x=anchor, **para_dict)(execute)()


def sut(x):
    def deco_sut(func):
        def execute_all():
            print(f"\n[testing function] {func.__name__}")
            for i, s in enumerate(suite, 1):  # run each test
                print(f"{i} [execute] {suite[s].name}" if suite[s].name
                      else f"{i} [execute] {s}")
                print(f"{i} [transformation] {suite[s].transformation.__name__}")
                print(f"{i} [relation] {suite[s].relation.__name__}")

                # para_dict: stores the args in @parametrized
                para_dict = dict(suite[s].parametrized)
                for k, v in para_dict.items():
                    para_dict[k] = st.sampled_from(v)

                suite_key(func=func, key=s, anchor=x, **para_dict)

        return execute_all

    return deco_sut
