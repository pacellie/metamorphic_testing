from metamorphic_test.transformation import MetamorphicTransformation


def shift(by: float) -> MetamorphicTransformation[float]:
    """A metamorphic transformation that shifts a float by the multiple of a given amount."""
    class Shift(MetamorphicTransformation[float]):
        def transform(self, anchor: float, multiple: int) -> float:
            return anchor + by * multiple
    return Shift()
