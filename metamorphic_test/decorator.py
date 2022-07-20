import pytest

from .helper import change_signature
from .generator import MetamorphicGenerator
from .suite import Suite, TestID


# A Suite maps module names with test names to the actual test instance
# Transformations and Relations can be registered as well as System under Tests.
# This needs to be a global, because there's no other way to register them in
# the proposed MT syntax our customer wants to use.
suite = Suite()


# name: name of the metamorphic test
# transform: optional transformation function
# relation: optional relation function
# (1) create a new instance of a metamorphic test
#     for now the transform just receives the default priority 0 -> change later?
# (2) retrieve the module of the caller of this function
# (3) register the test in the global suites variable
# (4) return the name as a handle to the caller
def metamorphic(name, *, transform=None, relation=None):
    test_id = suite.metamorphic(name)
    if transform is not None:
        suite.add_transform(test_id, transform, priority=0)
    if relation is not None:
        suite.set_relation(test_id, relation)
    return test_id


# randomize the argument arg by the value generated by the generator by setting
# overriding the value of arg in the given kwargs
def randomized(arg, generator: MetamorphicGenerator):
    def wrapper(transform):
        return suite.randomized_generator(transform, arg, generator)

    return wrapper


# fix the argument arg to the given value
# overriding the value of arg in the given kwargs
def fixed(arg, value):
    def wrapper(transform):
        return suite.fixed_generator(transform, arg, value)

    return wrapper


# metamorphic_name: name of a metamorphic test
# priority: priority of the transform
# transform: transformation function we are wrapping
# update the metamorphic test in the global suites variable by appending the
# (transform, priority) pair to the already present transformations of the given
# metamorphic test
def transformation(test_id, *, priority=0):
    def wrapper(transform):
        suite.add_transform(test_id, transform, priority=priority)
        return transform

    return wrapper


# metamorphic_name: name of a metamorphic test
# relation: relation function we are wrapping
# update the metamorphic test in the global suites variable by setting the relation
# of the given metamorphic test
def relation(*test_ids):
    def wrapper(relation):
        for test_id in test_ids:
            suite.set_relation(test_id, relation)
        return relation

    return wrapper


# test: the system under test function
# x: the actual input
# execute all the tests of this module in the global suites variable by delegating
# the the execute function of the MetamorphicTest class
def system(flag=None, *, name: TestID = None):
    def wrapper(test):
        @change_signature(test)
        def execute(*args, **kwargs):
            if kwargs:  # to be compatible with both given and pytest
                args = tuple(kwargs.values())
            if name is None:
                suite.execute_all(test, *args)
            else:
                suite.execute(name, test, *args)
            return suite

        return execute

    def mark_wrap(f):
        return pytest.mark.metamorphic(
            test_id=name,
            module=f.__module__,
        )(wrapper(f))

    if flag is None:
        return mark_wrap
    # flag is actually the function to be wrapped
    return mark_wrap(flag)