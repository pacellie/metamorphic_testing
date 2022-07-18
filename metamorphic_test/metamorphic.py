from dataclasses import dataclass, field
import random
from typing import Callable, Any, Optional, List

from .logger import logger


@dataclass
class PrioritizedTransform:
    transform: Callable[[Any], Any]
    priority: int = 0


Relation = Callable[[Any, Any], bool]

@dataclass
class MetamorphicTest:
    name: Optional[str] = None
    transforms: List[PrioritizedTransform] = field(
        default_factory=lambda: []
    )
    relation: Optional[Relation] = None


    def add_transform(self, transform, priority=0):
        self.transforms.append(PrioritizedTransform(transform, priority))

    def set_relation(self, relation):
        if self.relation:
            raise ValueError(f"Relation to {self.name} already set ({self.relation}).")
        self.relation = relation

    def _log_info(self, msg: str):
        logger.info(msg)


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

        if len(x) == 1:
            y = x[0]  # TODO: This is a bit weird
        else:
            y = x
        prio_sorted_transforms = sorted(
            self.transforms,
            key=lambda tp: tp.priority,
            reverse=True
        )
        for p_transform in prio_sorted_transforms:
            if len(x) == 1:
                y = p_transform.transform(y)
            else:
                y = p_transform.transform(*y)

        system_x = system(*x)
        if len(x) == 1:
            system_y = system(y)
        else:
            system_y = system(*y)

        transform_names = [
            p_transform.transform.__name__ for p_transform in self.transforms
        ]

        suite_text = f"[running suite '{self.name}']"
        input_x_text = f"input x: {x[0] if len(x) == 1 else x}"
        input_y_text = f"input y: {y}"
        output_x_text = f"output x: {system_x}"
        output_y_text = f"output y: {system_y}"
        transforms_text = f"transform: {', '.join(transform_names)}"
        relation_text = f"relation: {self.relation.__name__}"

        self._log_info(
            f"\n{suite_text}\n\t{input_x_text}\n\t{input_y_text}\n\t{output_x_text}"
            f"\n\t{output_y_text}\n\t{transforms_text}\n\t{relation_text}"
        )

        assert self.relation(system_x, system_y), \
            f"{suite_text}: {input_x_text} {input_y_text} {output_x_text}" \
                f"{output_y_text} {transforms_text} {relation_text}"
