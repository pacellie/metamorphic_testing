import pytest

from metamorphic_test.metamorphic import MetamorphicTest
from metamorphic_test.prioritized_transform import PrioritizedTransform

def double(x):
    return x * 2


def add2(x):
    return x + 2


def half(x):
    return x / 2


def minus2(x):
    return x - 2


def equal(x, y):
    return x == y


# 'add_transform':
#   * happy path
def test_add_transform():
    meta_test = MetamorphicTest()
    meta_test.add_transform(double)
    prio_transform = PrioritizedTransform(double, 0)

    assert prio_transform in meta_test.transforms

    index = meta_test.transforms.index(prio_transform)
    actual_prio_transform = meta_test.transforms[index]

    assert actual_prio_transform.transform == double # pylint: disable=comparison-with-callable


# 'set_relation':
#   * happy path
#   * double setting the relation raises
def test_set_relation():
    meta_test = MetamorphicTest()
    meta_test.set_relation(equal)

    assert meta_test.relation == equal # pylint: disable=comparison-with-callable


def test_set_relation_error():
    meta_test = MetamorphicTest()
    meta_test.set_relation(equal)

    with pytest.raises(ValueError):
        meta_test.set_relation(equal)


# 'execute':
#   * happy path with four transformations with relevant ordering
#   * no registered relation raises
#   * system raises
#   * relation raises
#   * transform raises
def test_execute():
    meta_test = MetamorphicTest()
    meta_test.set_relation(lambda _, y: y in (10, 11))

    meta_test.add_transform(minus2, 1)
    meta_test.add_transform(half, 0)
    meta_test.add_transform(add2, 2)
    meta_test.add_transform(double, 1)

    meta_test.execute(lambda x: x, 10)


def test_exexute_no_relation():
    meta_test = MetamorphicTest()

    with pytest.raises(ValueError):
        meta_test.execute(lambda x: x, 42)


def test_execute_system_raises():
    meta_test = MetamorphicTest()
    meta_test.set_relation(equal)

    def system(x):
        raise ValueError

    with pytest.raises(ValueError):
        meta_test.execute(system, 42)


def test_execute_relation_raises():
    meta_test = MetamorphicTest()

    def relation(x, y):
        raise ValueError

    meta_test.set_relation(relation)

    with pytest.raises(ValueError):
        meta_test.execute(lambda x: x, 42)


def test_execute_transform_raises():
    meta_test = MetamorphicTest()

    def transform(x):
        raise ValueError

    meta_test.set_relation(equal)
    meta_test.add_transform(transform)

    with pytest.raises(ValueError):
        meta_test.execute(lambda x: x, 42)
