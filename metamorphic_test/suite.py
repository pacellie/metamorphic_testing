import inspect
from collections import defaultdict
from functools import wraps

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

    def transformation(self, name, transform, *, priority):
        self.tests[f"{transform.__module__}.{name}"].transforms.append((transform, priority))

    def relation(self, name, relation):
        self.tests[f"{relation.__module__}.{name}"].relation = relation

    def execute(self, name, test_function, *args):
        assert name is not None
        self.tests[f"{test_function.__module__}.{name}"].execute(test_function, *args)

    def execute_all(self, test_function, *args):
        for full_name, m_test in self.tests.items():
            if full_name.startswith(f"{test_function.__module__}."):
                m_test.execute(test_function, *args)
