import pytest
from typing import Optional, TypeVar, Callable, Hashable

from .helper import change_signature
from .generator import MetamorphicGenerator
from .suite import Suite, TestID
from .transform import Transform
from .rel import Relation

A = TypeVar('A')

TransformWrapper = Callable[[Transform], Transform]
RelationWrapper = Callable[[Relation], Relation]
System = Callable


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
def metamorphic(
    name: str, *,
    transform: Optional[Transform] = None,
    relation: Optional[Relation] = None) -> TestID:

    test_id = suite.metamorphic(name)
    if transform is not None:
        suite.add_transform(test_id, transform, priority=0)
    if relation is not None:
        suite.set_relation(test_id, relation)
    return test_id


# randomize the argument arg by the value generated by the generator by setting
# overriding the value of arg in the given kwargs
def randomized(arg: str, generator: MetamorphicGenerator[A]) -> TransformWrapper:
    def wrapper(transform: Transform) -> Transform:
        return suite.randomized_generator(transform, arg, generator)

    return wrapper


# fix the argument arg to the given value
# overriding the value of arg in the given kwargs
def fixed(arg: str, value: A) -> TransformWrapper:
    def wrapper(transform: Transform) -> Transform:
        return suite.fixed_generator(transform, arg, value)

    return wrapper


# metamorphic_name: name of a metamorphic test
# priority: priority of the transform
# transform: transformation function we are wrapping
# update the metamorphic test in the global suites variable by appending the
# (transform, priority) pair to the already present transformations of the given
# metamorphic test
def transformation(test_id: TestID, *, priority: int = 0) -> TransformWrapper:
    def wrapper(transform: Transform) -> Transform:
        suite.add_transform(test_id, transform, priority=priority)
        return transform

    return wrapper


# metamorphic_name: name of a metamorphic test
# relation: relation function we are wrapping
# update the metamorphic test in the global suites variable by setting the relation
# of the given metamorphic test
def relation(*test_ids: TestID) -> RelationWrapper:
    def wrapper(relation: Relation) -> Relation:
        for test_id in test_ids:
            suite.set_relation(test_id, relation)
        return relation

    return wrapper


# names: the names of the metamorphic tests to be run
# test: the system under test function
# name: the name of the metamorphic test to be run
# x: the actual input
# execute all the tests of this module in the global suites variable by delegating
# the the execute function of the MetamorphicTest class
def system(*names: Hashable, **kwargs) -> Callable[[System], Callable[..., None]]:
    def wrapper(test: System) -> Callable[..., None]:
        @change_signature(test)
        def execute(name: str, *args, **kwargs):
            if kwargs:
                args = tuple(kwargs.values())
            suite.execute(name, test, *args)

        return pytest.mark.metamorphic(
            visualize_input=kwargs.get('visualize_input', None),
            visualize_output=kwargs.get('visualize_output', None),
        )(
            pytest.mark.parametrize('name', names)(execute)
        )

    return wrapper