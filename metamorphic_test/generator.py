from abc import ABCMeta


class MetamorphicGenerator(metaclass=ABCMeta):
    """
    This is an Abstract Base class for defining custom generators for generating
    randomized inputs by drawing values from a pool of values.

    This class must be inherited to define a new random input generator and the
    generate() method must be implemented.
    """
    def generate(self):
        ...
