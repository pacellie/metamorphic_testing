from metamorphic_test.transformation import MetamorphicTransformation


class Shift(MetamorphicTransformation[complex, complex]):
    """A metamorphic transformation that shifts a float by the multiple of a given amount."""
    def __init__(self, by: float):
        self.by = by

    def transform(self, anchor: complex, multiple: int = 1) -> complex:
        return anchor + self.by * multiple