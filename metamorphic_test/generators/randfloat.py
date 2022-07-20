import random

from metamorphic_test.generator import MetamorphicGenerator


class RandFloat(MetamorphicGenerator):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
    def generate(self):
        return random.uniform(self.min_value, self.max_value)  # nosec
