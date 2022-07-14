import inspect
from collections import defaultdict
from functools import wraps
from types import FunctionType

from .metamorphic import MetamorphicTest


class Suite:
    def __init__(self):
        self.tests = defaultdict(MetamorphicTest)

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

    def metamorphic(self, name, *, transform, relation):
        module = self.get_caller_module()
        test = MetamorphicTest(name=name,
                               transforms=[(transform, 0)],
                               relation=relation)

        self.tests[f"{module}.{name}"] = test

    def _get_test(self, function_in_module: FunctionType, name: str) -> MetamorphicTest:
        """Get the metamorphic test for the module of the given function and name."""
        return self.tests[f"{function_in_module.__module__}.{name}"]

    def transformation(self, name, transform, *, priority):
        self._get_test(transform, name).transforms.append((transform, priority))

    def relation(self, name, relation):
        self._get_test(relation, name).relation = relation

    def execute(self, name, test_function, *args):
        assert name is not None
        self._get_test(test_function, name).execute(test_function, *args)

    def _belongs_to(self, test_id: str, module_name: str) -> bool:
        """Check if the given test belongs to the given module."""
        return test_id.startswith(f"{module_name}.")

    def execute_all(self, test_function, *args):
        for full_name, m_test in self.tests.items():
            if self._belongs_to(full_name, test_function.__module__):
                m_test.execute(test_function, *args)
