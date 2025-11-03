"""
Evaluation function for chess positions.
Positive values favor White, negative values favor Black.
"""

from src import Board
from .material import evaluate as material
from .pst import evaluate as pst
from .pawn_structure import evaluate as pawn_structure
from .mobility import evaluate as mobility  # Slow, requires call `generate_legal_moves`

EVALUATION_FUNCTIONS = [material, pst, pawn_structure, mobility]


def evaluate(board: Board) -> int:
    """
    Board evaluation function that can be used by agents.
    """
    total_score = 0
    for eval_func in EVALUATION_FUNCTIONS:
        total_score += eval_func(board)
    return total_score
