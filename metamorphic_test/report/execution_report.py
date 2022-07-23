from contextlib import contextmanager
from typing import Callable, Generic, List, TypeVar

from metamorphic_test.prioritized_transform import PrioritizedTransform


T = TypeVar("T")


class FunctionOutput(Generic[T]):
    """The output of a function. Might have an error or a value."""

    def __init__(self):
        self._set = False
        self._output: T = None
        self._error: Exception = None
    
    @property
    def output(self) -> T:
        return self._output
    
    @output.setter
    def output(self, value: T):
        if self._set:
            raise ValueError("Output already set.")
        self._set = True
        self._output = value
    
    @property
    def error(self) -> Exception:
        return self._error
    
    @error.setter
    def error(self, value: Exception):
        if self._set:
            raise ValueError("Output already set.")
        self._set = True
        self._error = value
    
    def __str__(self):
        if self._set:
            if self.error:
                return f"error: {self.error}"
            return f"{self.output}"
        return "(unset)"


TransformOutput = FunctionOutput
SystemOutput = FunctionOutput
RelationOutput = FunctionOutput[bool]


class MetamorphicExecutionReport:
    """
    An execution report is a summary of a whole metamorphic test execution.

    It captures the details shown here:

    input_x ---------------- system ------> output_x
    | (transform 0)                            |
    transform_result[0]                        |
    | (transform 1)                            | (relation) (holds?)
    transform_result[1]                        |
    | ...                                      |
    transform_result[-1] --- system ------> output_y
    """
    def __init__(self,
        input_x,
        system: Callable,
        relation: Callable
    ):
        self.input_x = input_x
        self._transforms: List[PrioritizedTransform] = []
        self.transform_results: List[TransformOutput] = []
        self.system = system
        self.output_x: SystemOutput = SystemOutput()
        self.output_y: SystemOutput = SystemOutput()
        self.relation = relation
        self.relation_result = RelationOutput()
    
    @property
    def transforms(self) -> List[PrioritizedTransform]:
        return self._transforms
    
    @transforms.setter
    def transforms(self, value: List[PrioritizedTransform]):
        """List of PrioritizedTransform-s for the metamorphic test."""
        self._transforms = value
        self.transform_results = [TransformOutput() for _ in value]
    
    @contextmanager
    def register_transform_result(self, i: int):
        """
        Context manager for registering a transform result or an error.
        Usage:

        >>> with report.register_transform_result(0) as set_:
                # do the transformation
                result = transform(something)
                set_(result)
        
        This will set the result of the transform at index 0 in the report
        and store raised exceptions, if any.
        """
        assert 0 <= i < len(self.transforms)
        try:
            def set_(t):
                self.transform_results[i].output = t
            yield set_
        except Exception as e:
            self.transform_results[i].error = e
            raise e
    
    @contextmanager
    def register_output_x(self):
        """Context manager similar to register_transform_result."""
        try:
            def set_(x):
                self.output_x.output = x
            yield set_
        except Exception as e:
            self.output_x.error = e
            raise e

    @contextmanager
    def register_output_y(self):
        """Context manager similar to register_transform_result."""
        try:
            def set_(y):
                self.output_y.output = y
            yield set_
        except Exception as e:
            self.output_y.error = e
            raise e
    
    @contextmanager
    def register_relation_result(self):
        """Context manager similar to register_transform_result."""
        try:
            def set_(r):
                self.relation_result.output = r
            yield set_
        except Exception as e:
            self.relation_result.error = e
            raise e