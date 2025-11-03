"""
Evaluation function for chess positions.
Positive values favor White, negative values favor Black.
"""

from src import Board, GameStatus
from .material import evaluate as material
from .pst import evaluate as pst
from .pawn_structure import evaluate as pawn_structure
from .mobility import evaluate as mobility

# Evaluation functions and their weights, continuously
# tuned based on bot performance.
EVALUATION_FUNCTIONS_TO_WEIGHTS = {
    material: 1,
    pst: 1,
    pawn_structure: 1,
    # mobility: 1,  # Too expensive, requires call to `generate_legal_moves` each time
}


def evaluate(board: Board) -> int:
    """
    Board evaluation function that can be used by agents.
    """
    # Check for terminal positions (besides checkmate/stalemate,
    # since too expensive to compute per evaluation)
    if board.is_technical_draw():
        return 0

    total_score = 0
    for eval_func, weight in EVALUATION_FUNCTIONS_TO_WEIGHTS.items():
        total_score += eval_func(board) * weight
    return total_score
