from dataclasses import dataclass
from typing import Callable, Any, Optional


@dataclass
class Suite:
    name: Optional[str] = None
    transform: Optional[Callable[[Any], Any]] = None
    relation: Optional[Callable[[Any, Any], bool]] = None
