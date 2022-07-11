from dataclasses import dataclass, field
from typing import Callable, Any, Optional, List, Tuple
import random


@dataclass
class MetamorphicTest:
    name: Optional[str] = None
    transforms: List[Tuple[Callable[[Any], Any], int]] = field(default_factory=list)
    relation: Optional[Callable[[Any, Any], bool]] = None

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
