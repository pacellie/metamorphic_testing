from dataclasses import dataclass, field
from typing import Callable, Any, Optional, List, Tuple
import random


@dataclass
class MetamorphicTest:
    name: Optional[str] = None
    transforms: List[Tuple[Callable[[Any], Any], int]] = field(default_factory=list)
    relation: Optional[Callable[[Any, Any], bool]] = None

    def execute(self, system, *x):
        random.shuffle(self.transforms)

        y = x[0] if len(x) == 1 else x
        for transform, _ in sorted(self.transforms, key=lambda tp: tp[1], reverse=True):
            if transform.__name__ == 'identity':
                continue
            y = transform(y) if len(x) == 1 else transform(*y)

        transforms = [
            transform.__name__ for transform, _ in self.transforms
            if transform.__name__ != 'identity'
        ]

        system_x = system(*x)
        system_y = system(y) if len(x) == 1 else system(*y)

        print(f"\n[running suite '{self.name}']"
              f"\n\tinput x: {x[0] if len(x) == 1 else x} "
              f"\n\tinput y: {y} "
              f"\n\toutput x: {system_x} "
              f"\n\toutput y: {system_y} "
              f"\n\ttransform: {transforms} "
              f"\n\trelation: {self.relation.__name__}")

        assert self.relation(system_x, system_y)
