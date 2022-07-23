import random

from metamorphic_test.generator import MetamorphicGenerator


class RandInt(MetamorphicGenerator[int]):
    """ This is a custom random integer generator """
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        """
        min_value : int
            minimum value of the range
        """
        self.max_value = max_value
        """
        max_value : int
            maximum value of the range
        """

    def generate(self) -> int:
        """
        Returns a random integer from the closed interval [self.min_value, self.max_value]
        """
        return random.randint(self.min_value, self.max_value)  # nosec
