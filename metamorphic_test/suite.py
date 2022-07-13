import inspect
from collections import defaultdict
from .metamorphic import MetamorphicTest


class Suite:
    def __init__(self):
        self.suite = defaultdict(lambda: defaultdict(MetamorphicTest))

    @staticmethod
    def get_caller_module():
        frame = inspect.stack()[3]
        module = inspect.getmodule(frame[0])
        return module.__name__

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
        for s in self.suite[test.__module__]:
            if name and s != name:
                continue

            self.suite[test.__module__][s].execute(test, *args)
