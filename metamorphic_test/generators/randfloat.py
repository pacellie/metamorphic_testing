import random

from metamorphic_test.generator import MetamorphicGenerator


class RandFloat(MetamorphicGenerator[float]):
    def __init__(self, min_value: float, max_value: float) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def generate(self) -> float:
        return random.uniform(self.min_value, self.max_value)  # nosec
