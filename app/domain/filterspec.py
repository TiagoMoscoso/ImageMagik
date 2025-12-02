# filterspec.py
from dataclasses import dataclass
from typing import Callable, List, ParamSpec
import numpy as np

@dataclass
class FilterSpec:
    label: str
    params: List[ParamSpec]
    func: Callable[..., np.ndarray]
