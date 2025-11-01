"""
Constants and enumerations used throughout the chess engine.
"""

from enum import Enum, auto


class Color(Enum):
    """Represents the color of a chess piece."""

    WHITE = 0
    BLACK = 1


class PieceType(Enum):
    """Represents the type of a chess piece."""

    PAWN = (auto(), 1, "P", False)
    KNIGHT = (auto(), 3, "N", True)
    BISHOP = (auto(), 3, "B", True)
    ROOK = (auto(), 5, "R", True)
    QUEEN = (auto(), 9, "Q", True)
    KING = (auto(), 200, "K", False)

    def __init__(self, id, score, char, is_promotable):
        self.id = id
        self.score = score  # can't use 'value', reserved by Enum
        self.char = char
        self.is_promotable = is_promotable
