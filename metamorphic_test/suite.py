from functools import wraps
import inspect
from typing import Dict, TypeVar, Callable, Hashable

from .metamorphic import MetamorphicTest
from .generator import MetamorphicGenerator
from .logger import logger
from .transform import Transform
from .rel import Relation

A = TypeVar('A')


TestID = Hashable  # only guarantee made for outside use


class Suite:
    def __init__(self) -> None:
        self.tests: Dict[TestID, MetamorphicTest] = {}

    def get_test(self, test_id: TestID) -> MetamorphicTest:
        return self.tests[test_id]

    @staticmethod
    def get_caller_module() -> str:
        frame = inspect.stack()[3]
        module = inspect.getmodule(frame[0])
        if module is None:
            raise ValueError('Internal Error: no calling module.')
        return module.__name__

    @staticmethod
    def fixed_generator(transform: Transform, arg: str, value: A) -> Transform:
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

        @wraps(transform)
        def wrapper(*args, **kwargs):
            kwargs[arg] = generator.generate()
            return transform(*args, **kwargs)

        return wrapper

    def metamorphic(self, name: str) -> TestID:
        """
        Register a metamorphic test.
        Returns an identifier to later add relations / transforms to it if needed.
        """
        module = self.get_caller_module()
        test_id = f"{module}.{name}"
        if test_id in self.tests:
            raise ValueError(f"Test {test_id} already exists.")
        self.tests[test_id] = MetamorphicTest(name=name)
        return test_id

    def add_transform(
        self,
        test_id: TestID,
        transform: Transform, *,
        priority: int = 0) -> None:

        self.tests[test_id].add_transform(transform, priority)

    def set_relation(self, test_id: TestID, relation: Relation) -> None:
        self.tests[test_id].set_relation(relation)

    def execute(self, test_id: TestID, test_function: Callable, *args: tuple) -> None:
        assert test_id is not None, "Test id is 'None'"
        logger.debug(
            "Executing %test_id in %(test_function)", # type: ignore
            test_id=test_id,
            test_function=test_function.__module__
        )
        self.tests[test_id].execute(test_function, *args)
