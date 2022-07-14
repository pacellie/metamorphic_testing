import inspect
from collections import defaultdict
from functools import wraps
import logging

from .metamorphic import MetamorphicTest


class Suite:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.suite = defaultdict(lambda: defaultdict(MetamorphicTest))

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

        self.suite[module][name] = test

    def transformation(self, name, transform, *, priority):
        self.suite[transform.__module__][name].transforms.append((transform, priority))

    def relation(self, name, relation):
        self.suite[relation.__module__][name].relation = relation

    def execute(self, name, test, *args):
        which_names = f"test with name {name}" if name else "all tests"
        self.logger.debug(f"\nExecuting {which_names} inside {test.__module__}")
        for s in self.suite[test.__module__]:
            if name and s != name:
                continue

            self.suite[test.__module__][s].execute(test, *args)
