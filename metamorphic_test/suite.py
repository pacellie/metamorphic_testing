from functools import wraps
import inspect
import logging
from typing import Dict, Hashable

from .metamorphic import MetamorphicTest


TestID = Hashable  # only guarantee made for outside use


class Suite:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.tests: Dict[TestID, MetamorphicTest] = {}

    @staticmethod
    def get_caller_module():
        frame = inspect.stack()[3]
        module = inspect.getmodule(frame[0])
        return module.__name__

    @staticmethod
    def randomized_generator(transform, arg, generator):
        @wraps(transform)
        def wrapper(*args, **kwargs):
            kwargs[arg] = generator() if callable(generator) else generator
            return transform(*args, **kwargs)

        return wrapper

    def metamorphic(self, name) -> TestID:
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

    def add_transform(self, test_id: TestID, transform, *, priority=0):
        self.tests[test_id].add_transform(transform, priority)

    def set_relation(self, test_id: TestID, relation):
        self.tests[test_id].set_relation(relation)

    def execute(self, test_id, test_function, *args):
        assert test_id is not None, "Use execute_all"
        self.logger.debug(
            "Executing %test_id in %(test_function)",
            test_id=test_id,
            test_function=test_function.__module__
        )
        self.tests[test_id].execute(test_function, *args)

    def _belongs_to(self, test_id: str, module_name: str) -> bool:
        """Check if the given test belongs to the given module."""
        return test_id.startswith(f"{module_name}.")

    def execute_all(self, test_function, *args):
        self.logger.debug(
            "Executing all tests in %(test_function)",
            test_function=test_function.__module__
        )
        for full_name, m_test in self.tests.items():
            if self._belongs_to(full_name, test_function.__module__):
                self.logger.debug(
                    "Executing %(full_name)",
                    full_name=full_name
                )
                m_test.execute(test_function, *args)
