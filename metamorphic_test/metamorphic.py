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
    name: Optional[str] = None
    transforms: List[PrioritizedTransform] = field(
        default_factory=lambda: []
    )
    relation: Optional[Relation] = None
    reports: List[MetamorphicExecutionReport] = field(
        default_factory=lambda: []
    )


    def add_transform(self, transform: Transform, priority:int = 0) -> None:
        self.transforms.append(PrioritizedTransform(transform, priority))

    def set_relation(self, relation: Relation) -> None:
        if self.relation:
            raise ValueError(f"Relation to {self.name} already set ({self.relation}).")
        self.relation = relation


    # x: the actual input
    # system: the system under test
    # Idea: given tansformations (t1, 0), (t2, 0), (t3, 1), (t4, 2) which have been registered
    #       in any order we want to apply them either in order t4, t3, t2, t1 or t4, t3, t1,
    #       t2. In other words: higher priority means first, same priority means random order.
    # (1) shuffle all transforms
    # (2) sort the transforms by priority
    # Note: (1) + (2) implements the idea above
    # (3) apply the transforms one after the other two the input 'x' to obtain the output 'y'
    # (4) print some logging information
    # (5) apply the system under test and assert the relation function
    def execute(self, system: Callable, *x: tuple) -> None:
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

        succesfull_system_x = False
        succesfull_system_y = False
        succesfull_relation = False

        try:
            with report.register_output_x() as set_:
                system_x = system(*x)
                succesfull_system_x = True
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
                succesfull_system_y = True
                set_(system_y)

            with report.register_relation_result() as set_:
                relation_result = self.relation(system_x, system_y)
                succesfull_relation = True
                set_(relation_result)

            assert relation_result, \
                f"{self.name} failed: " \
                f"x: {x[0] if singular else x}, " \
                f"transform: {', '.join([t.get_name() for t in prio_sorted_transforms])}, " \
                f"relation: {self.relation.__name__}"
        finally:
            self.reports.append(report)
            msg = f"\n{StringReportGenerator(report).generate()}\n"
            if succesfull_system_x and succesfull_system_y and succesfull_relation and \
                relation_result:
                logger.info(msg)
            else:
                logger.error(msg)
