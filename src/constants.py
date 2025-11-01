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

    PAWN = (auto(), 1, "P")
    KNIGHT = (auto(), 3, "N")
    BISHOP = (auto(), 3, "B")
    ROOK = (auto(), 5, "R")
    QUEEN = (auto(), 9, "Q")
    KING = (auto(), 200, "K")

    def __init__(self, id, score, char):
        self.id = id
        self.score = score  # can't use 'value', reserved by Enum
        self.char = char
