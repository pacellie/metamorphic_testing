from dataclasses import dataclass, field
from typing import Callable, Any, Optional, List, Tuple
import random


@dataclass
class MetamorphicTest:
    name: Optional[str] = None
    # list of (transform, priority) pairs
    transforms: List[Tuple[Callable[[Any], Any], int]] = field(default_factory=list)
    relation: Optional[Callable[[Any, Any], bool]] = None

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
    def execute(self, x, system):
        random.shuffle(self.transforms)

        y = x
        for transform, _ in sorted(self.transforms, key=lambda tp: tp[1], reverse=True):
            y = transform(y)

        transforms = [
            transform.__name__ for transform, _ in self.transforms
            if transform.__name__ != 'identity'
        ]

        print(f"[running suite '{self.name}']"
              f"\n\tinput: {x} "
              f"\n\ttransform: {transforms} "
              f"\n\trelation: {self.relation.__name__}")

        assert self.relation(system(x), system(y))
