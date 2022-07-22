from dataclasses import dataclass, field
import random
from typing import Callable, Any, Optional, List

from metamorphic_test.report.execution_report import MetamorphicExecutionReport
from metamorphic_test.report.string_generator import StringReportGenerator
from .prioritized_transform import PrioritizedTransform

from .logger import logger

Relation = Callable[[Any, Any], bool]


@dataclass
class MetamorphicTest:
    """
    This class holds a single metamorphic test object along with its associated
    transformations and relation and provides a mechanism to execute the test.

    Attributes
    ----------
    name : str
        name of the metamorphic test. This is optional but rally useful when there
        are multiple metamorphic tests or some relation or transformation needs to
        be added to the test at later point of time after itS creation.

    transformation : List[PrioritizedTransform]
        a list of transformations to be applied on the source input to perform the
        metamorphic test.

    relation : Optional[Relation]
        a function that compares the source test case output to followup test case
        output and returns True if the relation holds, False otherwise.

    reports : List[MetamorphicExecutionReport]
        a list of objects of MetamorphicExecutionReport which hold the reports generation
        and logging logics for corresponding metamorphic tests.

    See Also
    --------
    decorator.metamorphic : Registers a new metamorphic test
    suite.Suite.metamorphic : This method is internally called by decorator.metamorphic()
                            to register a metamorphic test
    """
    name: Optional[str] = None
    transforms: List[PrioritizedTransform] = field(
        default_factory=lambda: []
    )
    relation: Optional[Relation] = None
    reports: List[MetamorphicExecutionReport] = field(
        default_factory=lambda: []
    )

    def add_transform(self, transform, priority=0):
        """
        Registers a transformation to a metamorphic test object

        Parameters
        ----------
        transform : callable
            a function (or any callable) to be used as a transformation
            for a particular metamorphic test. Ideally, this refers to
            the function decorated by decorator.transformation

        priority : int
            Optional keyword argument to set the order of the particular
            transformation of interest in a multiple transformation chain
            scenario. Default: 0

        See Also
        --------
        decorator.transformation : registers a decorated function as a
                                   transformation for a metamorphic test
        suite.Suite.add_transform : registers a function as a transformation
                                  to a metamorphic test
        """
        self.transforms.append(PrioritizedTransform(transform, priority))

    def set_relation(self, relation):
        """
        Registers a relation to a metamorphic test object

        Parameters
        ----------
        relation : Relation
            a function that compares the source test case output to followup test
            case output and returns True if the relation holds, False otherwise.

        See Also
        --------
        decorator.relation : registers a function as a relation for a metamorphic test
        suite.Suite.set_relation : registers a function as a relation to a metamorphic test
        """
        if self.relation:
            raise ValueError(f"Relation to {self.name} already set ({self.relation}).")
        self.relation = relation

    # x: the actual input
    # system: the system under test
    # Idea: given transformations (t1, 0), (t2, 0), (t3, 1), (t4, 2) which have been registered
    #       in any order we want to apply them either in order t4, t3, t2, t1 or t4, t3, t1,
    #       t2. In other words: higher priority means first, same priority means random order.
    # (1) shuffle all transforms
    # (2) sort the transforms by priority
    # Note: (1) + (2) implements the idea above
    # (3) apply the transforms one after the other two the input 'x' to obtain the output 'y'
    # (4) print some logging information
    # (5) apply the system under test and assert the relation function
    def execute(self, system, *x):
        """
        Executes the metamorphic test defined in the object and generate
        reports

        Note: This method is internally called from suite.Suite.execute
              with corresponding test_id

        Parameters
        ----------
        system : callable
            a function (or callable) which needs to be tested. This refers to the
            function decorated with decorator.system

        x : Any
            actual inputs for the system under test

        See Also
        --------
        decorator.system : Identifies the function decorated with this decorator as
                           a SystemUnderTest and executes all the metamorphic tests
        suite.Suite.execute : Execute a metamorphic test on a system under test
        """
        if not self.relation:
            raise ValueError(
                f"No relation registered on {self.name}, cannot execute test."
            )

        random.shuffle(self.transforms)

        report = MetamorphicExecutionReport(
            x[0] if len(x) == 1 else x,
            system,
            self.relation
        )

        try:
            with report.register_output_x() as set_:
                system_x = system(*x)
                set_(system_x)

            if len(x) == 1:
                y = x[0]
            else:
                y = x
            prio_sorted_transforms = sorted(
                self.transforms,
                key=lambda tp: tp.priority,
                reverse=True
            )
            report.transforms = prio_sorted_transforms

            for i, p_transform in enumerate(prio_sorted_transforms):
                with report.register_transform_result(i) as set_:
                    if len(x) == 1:
                        y = p_transform.transform(y)
                    else:
                        y = p_transform.transform(*y)
                    set_(y)

            with report.register_output_y() as set_:
                if len(x) == 1:
                    system_y = system(y)
                else:
                    system_y = system(*y)
                set_(system_y)

            with report.register_relation_result() as set_:
                relation_result = self.relation(system_x, system_y)
                set_(relation_result)
            assert relation_result
        finally:
            self.reports.append(report)
            logger.info("\n%s\n", StringReportGenerator(report).generate())
