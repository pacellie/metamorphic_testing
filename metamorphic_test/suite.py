from dataclasses import dataclass, field
from typing import Callable, Any, Tuple, Optional, List


@dataclass
class Suite:
    name: Optional[str] = None
    transformation: Optional[Callable[[Any], Any]] = None
    parametrized: List[Tuple[str, List]] = field(default_factory=list)
    relation: Optional[Callable[[Any, Any], bool]] = None
