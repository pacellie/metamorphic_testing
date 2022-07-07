from dataclasses import dataclass, field
from typing import Callable, Any, Tuple


@dataclass
class Suite:
    name: str = None
    transformation: Callable[[Any], Any] = None
    parametrized: list[Tuple[str, list]] = field(default_factory=list)  # e.g. [("n", [1,2,3]), ("c", [0])]
    relation: Callable[[Any, Any], bool] = None

