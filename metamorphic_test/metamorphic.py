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
    name: Optional[str] = None
    transforms: List[PrioritizedTransform] = field(
        default_factory=lambda: []
    )
    relation: Optional[Relation] = None
    reports: List[MetamorphicExecutionReport] = field(
        default_factory=lambda: []
    )


    def add_transform(self, transform, priority=0):
        self.transforms.append(PrioritizedTransform(transform, priority))
    
    def set_relation(self, relation):
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
    def execute(self, system, *x):
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
