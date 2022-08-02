import pytest
import inspect

from metamorphic_test.helper import change_signature


def prototype(arg1, arg2):  # pylint: disable=unused-argument
    """The prototype function provides the argument specification to be used as source"""


def sig_to_tuple(func):
    """Changes the signature object of a function to tuple"""
    return tuple(inspect.signature(func).parameters.items())


def test_change_signature_function():
    """Decorator was applied to a function"""
    @change_signature(prototype)
    def function():
        pass

    # Tests return type
    assert callable(function)

    # Tests if the first argument 'name' is inserted
    assert 'name' in sig_to_tuple(function)[0]

    # Tests if the rest of arguments are matched
    assert sig_to_tuple(function)[1:] == sig_to_tuple(prototype)


def test_change_signature_staticmethod():
    """Decorator was applied to a staticmethod"""
    class Class:
        @change_signature(prototype)
        @staticmethod
        def function():
            pass

    assert callable(Class.function)
    assert 'name' in sig_to_tuple(Class.function)[0]
    assert sig_to_tuple(Class.function)[1:] == sig_to_tuple(prototype)


def test_change_signature_class_error():
    """Decorator was applied to a class"""
    @change_signature(prototype)
    class Class:
        pass

    with pytest.raises(RuntimeError):
        Class()


def test_change_signature_classmethod_error():
    """Decorator was applied to a classmethod"""
    class Class:
        @change_signature(prototype)
        @classmethod
        def function(cls):
            pass

    with pytest.raises(RuntimeError):
        Class.function()


def test_change_signature_instancemethod_error():
    """Decorator was applied to an instancemethod"""
    class Class:
        @change_signature(prototype)
        def function(self):
            pass

    with pytest.raises(RuntimeError):
        c = Class()
        Class.function(c)
