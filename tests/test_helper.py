import pytest
import inspect

from metamorphic_test.helper import change_signature


# The prototype function provides the argument specification to be sourced
def prototype(arg1, arg2):  # pylint: disable=unused-argument
    pass


# Changes the signature object of a function to tuple
def sig_to_tuple(func):
    return tuple(inspect.signature(func).parameters.items())


# 1. Decorator was applied to a function
def test_change_signature_function():
    @change_signature(prototype)
    def function():
        pass

    # Tests return type
    assert callable(function)

    # Tests if the first argument 'name' is inserted
    assert 'name' in sig_to_tuple(function)[0]

    # Tests if the rest of arguments are matched
    assert sig_to_tuple(function)[1:] == sig_to_tuple(prototype)


# 2. Decorator was applied to a staticmethod
def test_change_signature_staticmethod():
    # The class that its staticmethod function will be changed
    class Class:
        @change_signature(prototype)
        @staticmethod
        def function():
            pass

    assert callable(Class.function)
    assert 'name' in sig_to_tuple(Class.function)[0]
    assert sig_to_tuple(Class.function)[1:] == sig_to_tuple(prototype)


# 3. Decorator was applied to a class
def test_change_signature_class_error():
    @change_signature(prototype)
    class Class:
        pass

    with pytest.raises(RuntimeError):
        Class()


# 4. Decorator was applied to a classmethod
def test_change_signature_classmethod_error():
    class Class:
        @change_signature(prototype)
        @classmethod
        def function(cls):
            pass

    with pytest.raises(RuntimeError):
        Class.function()


# 5. Decorator was applied to an instancemethod
def test_change_signature_instancemethod_error():
    class Class:
        @change_signature(prototype)
        def function(self):
            pass

    with pytest.raises(RuntimeError):
        c = Class()
        Class.function(c)
