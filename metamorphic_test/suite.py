from functools import wraps
import inspect
from typing import Dict, TypeVar, Callable, Hashable, Tuple

from .metamorphic import MetamorphicTest
from .generator import MetamorphicGenerator
from .logger import logger
from .transform import Transform
from .rel import Relation

A = TypeVar('A')

TestID = Hashable  # only guarantee made for outside use


class Suite:
    """
    This class holds all the metamorphic tests along with corresponding
    transformations and relations and executes them on trigger.

    Although, decorators exposes easy and intuitive ways to register
    metamorphic tests, transformations, relations and executes all the
    metamorphic test on corresponding system under test functions,
    in the backend all decorated functions get registered to this class.

    See Also
    --------
    decorators.py
    """

    def __init__(self) -> None:
        self.tests: Dict[TestID, MetamorphicTest] = {}
        """
        tests : Dict[TestID, MetamorphicTest]
            A dictionary with keys as test_ids and values as metamorphic_tests
            to hold all the metamorphic tests within a single data structure.
        """

    def get_test(self, test_id: TestID) -> MetamorphicTest:
        """
        A method to get a metamorphic test from the internal dictionary
        containing all of the metamorphic tests.

        Parameters
        ----------
        test_id : TestID
            a hashable key for a metamorphic test of interest

        Returns
        -------
        metamorphic_test : MetamorphicTest
            a metamorphic test corresponding to the input test_id

        See Also
        --------
        decorator.metamorphic() : to register a metamorphic test from user
        metamorphic.MetaMorphicTest : to hold a metamorphic test along with
                                      relation and transformations

        """
        return self.tests[test_id]

    def get_test_id(self) -> Tuple[Hashable, ...]:
        """
        A method to get a metamorphic test_id from the internal dictionary
        containing all of the metamorphic tests.

        Returns
        -------
        test_id_list : Tuple[Hashable, ...]
            a list of test ids for the corresponding test module
        """
        module = self.get_caller_module()
        test_id_list = [
            k for k, _ in self.tests.items()
            if str(k).split('.', maxsplit=1)[0] == module
        ]
        return tuple(test_id_list)

    @staticmethod
    def get_caller_module() -> str:
        """
        A static method to get the name of the module where the test is created

        Returns
        -------
        name : str
            the module name where the test is created
        """
        # Returns a list of frame records for the caller's stack.
        # The first entry in the returned list represents the caller.
        # The third index gets the third caller where the test is created:
        # suite.py -> decorator.py -> test_*.py
        frame = inspect.stack()[3]
        module = inspect.getmodule(frame[0])
        if module is None:
            raise ValueError('Internal Error: no calling module.')
        return module.__name__

    @staticmethod
    def fixed_generator(transform: Transform, arg: str, value: A) -> Transform:
        """
        This method is internally called by decorator.fixed to register a fixed
        generator to a transformation.

        Parameters
        ----------
        transform : Transform
            the transformation to which the fixed_generator needs to be associated
            to always get a fixed value for an argument to the transformation.

        arg : str
            name of the argument which needs to be supplied with a fixed value while
            performing transformation

        value : A
            the fixed value for the argument arg

        Returns
        -------
        wrapper : callable
            a function which modifies the original transformation function by setting a
            given fixed value to one of its arguments.
            Please note: to set fixed values to multiple arguments of a transformation,
            use the fixed decorator multiple times

        See Also
        --------
        decorators.fixed : Fix the argument arg to the given value overriding the value
                           of arg in the given kwargs
        """

        @wraps(transform)
        def wrapper(*args, **kwargs):
            kwargs[arg] = value
            return transform(*args, **kwargs)

        return wrapper

    @staticmethod
    def randomized_generator(
            transform: Transform,
            arg: str,
            generator: MetamorphicGenerator[A]) -> Transform:
        """
        This method is internally called by decorator.randomized to register a
        randomized generator to a transformation.

        Parameters
        ----------
        transform : Transform
            the transformation to which the randomized_generator needs to be
            associated to always get a fixed value for an argument to the
            transformation.

        arg : str
            name of the argument which needs to be supplied with a randomized
            value while performing transformation

        generator: MetamorphicGenerator[A]
            the custom random generator for the argument arg

        Returns
        -------
        wrapper : Transform
            a function which modifies the original transformation function by setting a
            randomized value to one of its arguments.
            Please note: to set randomized values to multiple arguments of a transformation,
            use the randomized decorator multiple times

        See Also
        --------
        decorators.randomized : Randomize the argument arg by the value generated by
                                the generator
        """

        @wraps(transform)
        def wrapper(*args, **kwargs):
            kwargs[arg] = generator.generate()
            return transform(*args, **kwargs)

        return wrapper

    def metamorphic(self, name: str) -> TestID:
        """
        This method is internally called by decorator.metamorphic() to register a
        metamorphic test in self.tests attribute.

        Parameters
        ----------
        name : str
            name of the metamorphic test

        Returns
        -------
        test_id : TestID
            Returns a hashable identifier to later add relations / transforms to it
            if needed.

        See Also
        --------
        decorator.metamorphic : Registers a new metamorphic test
        """
        module = self.get_caller_module()
        test_id = f"{module}.{name}"
        if test_id in self.tests:
            raise ValueError(f"Test {test_id} already exists.")
        self.tests[test_id] = MetamorphicTest(name=name)
        return test_id

    def add_transform(self,
                      test_id: TestID,
                      transform: Transform, *,
                      priority: int = 0) -> None:
        """
        This method is internally called by decorator.transformation to
        register a function as a transformation to a metamorphic test.

        Parameters
        ----------
        test_id : TestID
            a hashable identifier for a metamorphic test

        transform : Transform
            a function (or any callable) to be used as a transformation
            for a particular metamorphic test. Ideally, this refers to
            the function decorated by decorator.transformation

        priority : int
            Optional keyword argument to set the order of the particular
            transformation of interest in a multiple transformation chain
            scenario. Default: 0

        See Also
        --------
        decorator.transformation : Registers a decorated function as a
                                   transformation for a metamorphic test
        metamorphic.MetamorphicTest : A data class to hold a metamorphic test object
                                      along with its transformations and relation
        """
        self.tests[test_id].add_transform(transform, priority)

    def set_relation(self, test_id: TestID, relation: Relation) -> None:
        """
        This method is internally called by decorator.relation to
        register a function as a relation to a metamorphic test.

        Parameters
        ----------
        test_id : TestID
            a hashable identifier for a metamorphic test

        relation : Relation
            a function (or any callable) to be used as a relation
            for a particular metamorphic test. Ideally, this refers to
            the function decorated by decorator.relation

            Please note: one metamorphic test can have only one relation
                         Attempt to add multiple relation to a same
                         metamorphic test will result in ValueError.

        See Also
        --------
        decorator.relation : registers a function as a relation for a metamorphic test
        metamorphic.MetamorphicTest : A data class to hold a metamorphic test object
                                      along with its transformations and relation
        """
        self.tests[test_id].set_relation(relation)

    def execute(self, test_id: TestID, test_function: Callable, *args: tuple) -> None:
        """
        Execute a metamorphic test identified by test_id on a system under test
        denoted by test_function

        Parameters
        ----------
        test_id : TestID
            a hashable identifier for a metamorphic test which needs to be executed

        test_function : Callable
            a function (or callable) which needs to be tested. This refers to the
            function decorated with decorator.system

        args : tuple
            actual arguments for the system under test

        See Also
        --------
        decorator.system : Identifies the function decorated with this decorator as
                           a SystemUnderTest and executes all the metamorphic tests
        metamorphic.MetamorphicTest : A data class to hold a metamorphic test object
                                      along with its transformations and relation
        """

        assert test_id is not None, "Test id is 'None'"
        logger.debug(
            "Executing %test_id in %(test_function)",  # type: ignore
            test_id=test_id,
            test_function=test_function.__module__
        )
        self.tests[test_id].execute(test_function, *args)
