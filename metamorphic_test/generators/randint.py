import random

from metamorphic_test.generator import MetamorphicGenerator


class RandInt(MetamorphicGenerator[int]):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def generate(self) -> int:
        return random.randint(self.min_value, self.max_value)  # nosec
