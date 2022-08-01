from dataclasses import dataclass

from .transform import Transform


@dataclass
class PrioritizedTransform:
    """
    This class associates a transformation function with a priority.

    See Also
    --------
    transform : The type of a transform
    metamorphic.MetamorphicTest.execute : This method internally constructs
        prioritized transforms to determine the evaluation order of the given
        transforms
    """
    transform: Transform
    """
    transform : Transform
        The transformation function.
    """
    priority: int = 0
    """
    priority : int
        The priority of the transformation function which defaults to 0.
    """

    def get_name(self) -> str:
        """
        Convenient access to the actual transformation's name.

        Returns:
        --------
        out : str
            The name of the actural transformation associated with the
            prioritized transform.
        """
        return self.transform.__name__