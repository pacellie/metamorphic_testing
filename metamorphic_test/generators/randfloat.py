import random

from metamorphic_test.generator import MetamorphicGenerator


class RandFloat(MetamorphicGenerator[float]):
    """
    This is a custom random floating point number generator

    Parameters
    ----------
    min_value : float
        minimum value of the range
    max_value : float
        maximum value of the range

    Attributes
    ----------
    min_value : float
        minimum value of the range
    max_value : float
        maximum value of the range
    """
    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        self.max_value = max_value

    def generate(self) -> float:
        """
        Returns a random floating point value from the closed interval
        [self.min_value, self.max_value]
        """
        return random.uniform(self.min_value, self.max_value)  # nosec
