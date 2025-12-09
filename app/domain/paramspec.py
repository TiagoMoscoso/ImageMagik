
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class ParamSpec:
    name: str
    ptype: str  
    default: Any
    min_val: float | int | None = None
    max_val: float | int | None = None
    step: float | int = 1
    options: Iterable[Any] | None = None 