"""
Evaluation function for chess positions.
Positive values favor White, negative values favor Black.
"""

from src import Board
from .material import material

EVALUATION_FUNCTIONS = [material]


def evaluate(board: Board) -> int:
    """
    Board evaluation function that can be used by agents.
    """
    # return sum(func(board) for func in EVALUATION_FUNCTIONS)

    # One line sum function looks cooler, but if my 1-year LeetCode streak
    # taught me anything, is that it's actually slower than a simple loop.
    total_score = 0
    for eval_func in EVALUATION_FUNCTIONS:
        total_score += eval_func(board)
    return total_score
