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

    PAWN = (auto(), 100, "P", False)
    KNIGHT = (auto(), 320, "N", True)
    BISHOP = (auto(), 330, "B", True)
    ROOK = (auto(), 500, "R", True)
    QUEEN = (auto(), 900, "Q", True)
    KING = (auto(), 20_000, "K", False)

    def __init__(self, id, centipawn_value, char, is_promotable):
        self.id = id
        self.centipawn_value = centipawn_value  # can't use 'value', reserved by Enum
        self.char = char
        self.is_promotable = is_promotable
