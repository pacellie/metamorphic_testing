import pytest

from metamorphic_test.metamorphic import MetamorphicTest
from metamorphic_test.prioritized_transform import PrioritizedTransform

def transform(x):
    return x * 2


def relation(x, y):
    return x == y


def test_add_transform():
    meta_test = MetamorphicTest()
    meta_test.add_transform(transform)
    prio_transform = PrioritizedTransform(transform, 0)

    assert prio_transform in meta_test.transforms

    index = meta_test.transforms.index(prio_transform)
    actual_prio_transform = meta_test.transforms[index]

    assert actual_prio_transform.transform == transform


def test_set_relation():
    meta_test = MetamorphicTest()
    meta_test.set_relation(relation)

    assert meta_test.relation == relation


def test_set_relation_error():
    meta_test = MetamorphicTest()
    meta_test.set_relation(relation)

    with pytest.raises(ValueError):
        meta_test.set_relation(relation)


