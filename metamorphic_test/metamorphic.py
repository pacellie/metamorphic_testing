from dataclasses import dataclass, field
from typing import Callable, Any, Optional, List
import random

from metamorphic_test.transforms import identity


@dataclass
class PrioritizedTransform:
    transform: Callable[[Any], Any]
    priority: int = 0


@dataclass
class MetamorphicTest:
    name: Optional[str] = None
    # list of (transform, priority) pairs
    transforms: List[PrioritizedTransform] = field(
        default_factory=lambda: []
    )
    relation: Optional[Callable[[Any, Any], bool]] = None


    def add_transform(self, transform, priority=0):
        if transform is not identity:
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
            raise ValueError("No relation registered, cannot execute test.")

        random.shuffle(self.transforms)

        prio_sorted_transforms = sorted(
            self.transforms,
            key=lambda tp: tp.priority,
            reverse=True
        )
        if len(x) == 1:
            y = x[0]  # TODO: This is a bit weird
        else:
            y = x
        for p_transform in prio_sorted_transforms:
            if len(x) == 1:
                y = p_transform.transform(y)
            else:
                y = p_transform.transform(*y)

        transforms = [
            p_transform.transform.__name__ for p_transform in self.transforms
        ]

        system_x = system(*x)
        if len(x) == 1:
            system_y = system(y)
        else:
            system_y = system(*y)

        print(f"\n[running suite '{self.name}']"
              f"\n\tinput x: {x[0] if len(x) == 1 else x} "
              f"\n\tinput y: {y} "
              f"\n\toutput x: {system_x} "
              f"\n\toutput y: {system_y} "
              f"\n\ttransform: {transforms} "
              f"\n\trelation: {self.relation.__name__}")

        assert self.relation(system_x, system_y)
