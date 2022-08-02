import pytest
import inspect
from unittest.mock import Mock, patch
from hypothesis import given
import hypothesis.strategies as st

from metamorphic_test.suite import Suite
from metamorphic_test.metamorphic import MetamorphicTest
from metamorphic_test.transform import Transform

NAME = 'a'


@pytest.fixture(scope='module')
def current_module_name():
    return inspect.getmodule(inspect.currentframe()).__name__


def test_get_test():
    suite = Suite()

    with pytest.raises(KeyError):
        suite.get_test(NAME)

    test_id = suite.metamorphic(NAME)
    test_object = suite.get_test(test_id)
    assert isinstance(test_object, MetamorphicTest)


def test_get_test_id(current_module_name):
    suite = Suite()
    assert not suite.get_test_id()

    suite.metamorphic(NAME)
    test_id = suite.get_test_id()
    assert isinstance(test_id, tuple)
    assert len(test_id) == len(test_id)
    assert NAME in str(test_id)

    assert f"{current_module_name}.{NAME}" in str(test_id)


def test_get_caller_module(current_module_name):
    suite = Suite()
    assert isinstance(suite.get_caller_module(), str)
    assert suite.get_caller_module() == current_module_name


def test_get_caller_module_error():
    suite = Suite()
    with patch('inspect.stack', lambda: []):
        with pytest.raises(ValueError):
            suite.get_caller_module()


@given(st.integers(-5, 5), st.integers(-5, 5))
def test_fixed_generator(value, fixed):
    suite = Suite()

    def transform(arg1, arg2):
        return arg1, arg2

    fixed_func = suite.fixed_generator(transform, 'arg2', fixed)
    assert isinstance(fixed_func, Transform)  # noqa
    assert fixed_func(value) == (value, fixed)


@given(st.integers(-5, 5), st.integers(-5, 5))
def test_randomized_generator(value, randomized):
    suite = Suite()

    def transform(arg1, arg2):
        return arg1, arg2

    generator = Mock()
    generator.generate.side_effect = lambda: randomized

    randomized_func = suite.randomized_generator(transform, 'arg2', generator)
    assert isinstance(randomized_func, Transform)  # noqa
    assert randomized_func(value) == (value, randomized)


def test_metamorphic(current_module_name):
    suite = Suite()
    mock_test_id = suite.metamorphic(NAME)

    assert isinstance(mock_test_id, str)
    assert current_module_name in mock_test_id
    assert NAME in mock_test_id
    assert f"{current_module_name}.{NAME}" == mock_test_id

    with pytest.raises(ValueError):
        suite.metamorphic(NAME)


@given(priority=st.integers(0, 5))
def test_add_transform(priority):
    suite = Suite()

    def transform():
        pass

    with pytest.raises(KeyError):
        suite.add_transform(NAME, transform)
        suite.add_transform(NAME, transform, priority=priority)

    test_id = suite.metamorphic(NAME)
    assert suite.add_transform(test_id, transform) is None
    assert suite.add_transform(test_id, transform, priority=priority) is None


def test_set_relation():
    suite = Suite()

    def relation() -> bool:
        pass

    with pytest.raises(KeyError):
        suite.set_relation(NAME, relation)

    test_id = suite.metamorphic(NAME)
    assert suite.set_relation(test_id, relation) is None


@given(args=st.tuples(st.integers(-5, 5), st.integers(-5, 5)))
def test_execute(args):
    suite = Suite()

    def system():
        pass

    with pytest.raises(KeyError):
        suite.execute(NAME, system, args)

    test_id = suite.metamorphic(NAME)
    with pytest.raises(ValueError):
        suite.execute(test_id, system, args)

    with pytest.raises(AssertionError):
        suite.execute(None, system, args)
        assert suite.execute(test_id, system, args)

    suite.execute = Mock(return_value=None)
    assert suite.execute(test_id, system, args) is None
