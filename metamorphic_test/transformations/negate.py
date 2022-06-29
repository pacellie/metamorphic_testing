from metamorphic_test.transformation import MetamorphicTransformation


class Negate(MetamorphicTransformation[complex, complex]):
    """A metamorphic transformation that negates any number."""
    def transform(self, anchor: complex) -> complex:
        return - anchor
