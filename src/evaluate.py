"""
Evaluation functions for chess positions.
Positive values favor White, negative values favor Black.
"""

from src import Board, Color


def material(board: Board) -> int:
    """
    Simple material evaluation.

    Returns:
        Evaluation score in centipawns
    """
    score = 0
    for rank in range(8):
        for file in range(8):
            piece = board.board[rank][file]
            if piece:
                value = piece.piece_type.centipawn_value
                if piece.color == Color.WHITE:
                    score += value
                else:
                    score -= value
    return score


def evaluate(board: Board) -> int:
    """
    Default evaluation function that can be used by agents.
    """
    return material(board)
