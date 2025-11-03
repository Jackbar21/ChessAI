"""
Evaluation function for chess positions.
Positive values favor White, negative values favor Black.
"""

from src import Board
from .material import evaluate as material
from .pst import evaluate as pst
from .pawn_structure import evaluate as pawn_structure
from .mobility import evaluate as mobility

EVALUATION_FUNCTIONS = [material, pst, pawn_structure, mobility]


def evaluate(board: Board) -> float:
    """
    Board evaluation function that can be used by agents.
    """
    # Check for terminal positions (besides checkmate/stalemate,
    # since too expensive to compute per evaluation)
    if board.is_technical_draw():
        return 0.0

    total_score = 0.0
    for eval_func in EVALUATION_FUNCTIONS:
        total_score += eval_func(board)
    return total_score
