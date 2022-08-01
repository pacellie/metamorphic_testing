from hypothesis import given
from hypothesis.strategies import integers

from metamorphic_test.decorator import (
    metamorphic,
    randomized,
    fixed,
    transformation,
    relation,
    system
)
import metamorphic_test.decorator as d
from metamorphic_test.suite import Suite
from metamorphic_test.metamorphic import MetamorphicTest
from metamorphic_test.prioritized_transform import PrioritizedTransform
from metamorphic_test.generator import MetamorphicGenerator


NAME = 'test'
INT = 42
ARG = 'n'


class FixedGenerator(MetamorphicGenerator[int]):
    def generate(self) -> int:
        return INT


def identity(x):
    return x


def multiply_by_n(x, n):
    return n * x


def equal(x, y):
    return x == y


def module_namify(name):
    return f'tests.test_decorator.{name}'


def test_metamorphic():
    d.suite = Suite()

    prio_transform = PrioritizedTransform(identity)
    metamorphic(NAME, transform=identity, relation=equal)

    meta_test = MetamorphicTest(NAME, transforms=[prio_transform], relation=equal)

    assert d.suite.get_test(module_namify(NAME)) == meta_test, \
        'calling metamorphic should register an instance of MetamorphicTest'


@given(integers())
def test_randomized(x):
    generator = FixedGenerator()
    rand_transform = randomized(ARG, generator)(multiply_by_n)

    assert rand_transform(x) == x * INT, \
        'randomizing a function is equivalent to calling it with a random value' \
        'for the same argument'


@given(integers())
def test_fixed(x):
    fixed_transform = fixed(ARG, INT)(multiply_by_n)

    assert fixed_transform(x) == x * INT, \
        'fixing a function is equivalent to calling it with a fixed value' \
        'for the same argument'


def test_transformation():
    d.suite = Suite()

    meta = metamorphic(NAME)
    returned_transform = transformation(meta)(identity)

    assert identity == returned_transform

    prio_transform = PrioritizedTransform(identity)
    meta_test = MetamorphicTest(NAME, transforms=[prio_transform])

    assert d.suite.get_test(module_namify(NAME)) == meta_test, \
        'calling transformation should return the same transform and register' \
        'it in the metamorphic test instance'



def test_relation():
    d.suite = Suite()

    meta = metamorphic(NAME)
    returned_rel = relation(meta)(equal)

    assert equal == returned_rel

    meta_test = MetamorphicTest(NAME, relation=equal)

    assert d.suite.get_test(module_namify(NAME)) == meta_test, \
        'calling relation should return the same relation and register' \
        'it in the metamorphic test instance'


@given(integers())
def test_system(x):
    d.suite = Suite()

    meta = metamorphic(NAME, transform=identity, relation=equal)

    system(meta)(identity)(module_namify(NAME), x)  # system already asserts
