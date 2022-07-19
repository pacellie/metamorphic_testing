from abc import ABCMeta


class MetamorphicGenerator(metaclass=ABCMeta):
    def generate(self):
        ...
