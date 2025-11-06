from enum import Enum, auto
from src import Move
from dataclasses import dataclass
from typing import Optional


class BoundType(Enum):
    EXACT = auto()
    LOWERBOUND = auto()
    UPPERBOUND = auto()


@dataclass
class TTEntry:
    value: float
    depth: int
    flag: BoundType
    best_move: Optional[Move]  # Move | None
