from dataclasses import dataclass, field
import logging
import random
from typing import Callable, Any, Optional, List


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
        # https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/ indicates
        # that getting the logger in module_level is a bad idea, hence inside the function.
        # Weirdly that contradicts this, which recommend module-logging:
        # https://coralogix.com/blog/python-logging-best-practices-tips/
        logger = logging.getLogger(__name__)
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

        self._log_info(f"\n[running suite '{self.name}']"
              f"\n\tinput x: {x[0] if len(x) == 1 else x} "
              f"\n\tinput y: {y} "
              f"\n\toutput x: {system_x} "
              f"\n\toutput y: {system_y} "
              f"\n\ttransform: {', '.join(transform_names)} "
              f"\n\trelation: {self.relation.__name__}")

        assert self.relation(system_x, system_y)
