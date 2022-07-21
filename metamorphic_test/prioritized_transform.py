from dataclasses import dataclass

from .transform import Transform


@dataclass
class PrioritizedTransform:
    transform: Transform
    priority: int = 0

    def get_name(self) -> str:
        return self.transform.__name__