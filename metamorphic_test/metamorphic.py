from dataclasses import dataclass, field
import random
from typing import Callable, Optional, List

from metamorphic_test.report.execution_report import MetamorphicExecutionReport
from metamorphic_test.report.string_generator import StringReportGenerator
from .prioritized_transform import PrioritizedTransform
from .transform import Transform
from .rel import Relation
from .logger import logger


@dataclass
class MetamorphicTest:
    """
    This class holds a single metamorphic test object along with its associated
    transformations and relation and provides a mechanism to execute the test.

    See Also
    --------
    decorator.metamorphic : Registers a new metamorphic test
    suite.Suite.metamorphic : This method is internally called by decorator.metamorphic()
                            to register a metamorphic test
    """
    name: Optional[str] = None
    """
    name : str
        name of the metamorphic test. This is optional but really useful when there
        are multiple metamorphic tests or some relation or transformation needs to
        be added to the test at later point of time after itS creation.
    """

    transforms: List[PrioritizedTransform] = field(
        default_factory=lambda: []
    )
    """
    transformation : List[PrioritizedTransform]
        a list of transformations to be applied on the source input to perform the
        metamorphic test.
    """

    relation: Optional[Relation] = None
    """
    relation : Optional[Relation]
        a function that compares the source test case output to followup test case
        output and returns True if the relation holds, False otherwise.
    """

    reports: List[MetamorphicExecutionReport] = field(
        default_factory=lambda: []
    )
    """
    reports : List[MetamorphicExecutionReport]
        a list of objects of MetamorphicExecutionReport which hold the reports generation
        and logging logics for corresponding metamorphic tests.
    """

    def add_transform(self, transform: Transform, priority: int = 0) -> None:
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

    def set_relation(self, relation: Relation) -> None:
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
    def execute(self, system: Callable, *x: tuple) -> None:
        # pylint: disable-msg=too-many-locals
        """
        Executes the metamorphic test defined in the object and generate
        reports

        Note: This method is internally called from suite.Suite.execute
              with corresponding test_id

        Parameters
        ----------
        system : Callable
            a function (or callable) which needs to be tested. This refers to the
            function decorated with decorator.system

        x : tuple
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

        singular = len(x) == 1

        report = MetamorphicExecutionReport(
            x[0] if singular else x,
            system,
            self.relation
        )

        successful_system_x = False
        successful_system_y = False
        successful_relation = False

        try:
            with report.register_output_x() as set_:
                system_x = system(*x)
                successful_system_x = True
                set_(system_x)

            y = x[0] if singular else x
            prio_sorted_transforms = sorted(
                self.transforms,
                key=lambda tp: tp.priority,
                reverse=True
            )
            report.transforms = prio_sorted_transforms

            for i, p_transform in enumerate(prio_sorted_transforms):
                with report.register_transform_result(i) as set_:
                    y = p_transform.transform(y) if singular else p_transform.transform(*y)
                    set_(y)

            with report.register_output_y() as set_:
                system_y = system(y) if singular else system(*y)
                successful_system_y = True
                set_(system_y)

            with report.register_relation_result() as set_:
                relation_result = self.relation(system_x, system_y)
                successful_relation = True
                set_(relation_result)

            assert relation_result, \
                f"{self.name} failed: " \
                f"x: {x[0] if singular else x}, " \
                f"transform: {', '.join([t.get_name() for t in prio_sorted_transforms])}, " \
                f"relation: {self.relation.__name__}"
        finally:
            self.reports.append(report)
            msg = f"\n{StringReportGenerator(report).generate()}\n"
            if successful_system_x and successful_system_y and successful_relation and \
                    relation_result:
                logger.info(msg)
            else:
                logger.error(msg)
