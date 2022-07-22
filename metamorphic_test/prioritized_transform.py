from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class PrioritizedTransform:
    transform: Callable[[Any], Any]
    priority: int = 0

    def get_name(self):
        return self.transform.__name__