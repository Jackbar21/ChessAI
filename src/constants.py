"""
Constants and enumerations used throughout the chess engine.
"""

from enum import Enum


class Color(Enum):
    """Represents the color of a chess piece."""

    WHITE = 0
    BLACK = 1


class PieceType(Enum):
    """Represents the type of a chess piece."""

    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5


PIECE_VALUES = {
    PieceType.PAWN: 1,
    PieceType.KNIGHT: 3,
    PieceType.BISHOP: 3,
    PieceType.ROOK: 5,
    PieceType.QUEEN: 9,
    PieceType.KING: 200,  # Arbitrarily high value, not inf. for eval function
}

PIECE_CHARS = {
    PieceType.PAWN: "P",
    PieceType.KNIGHT: "N",
    PieceType.BISHOP: "B",
    PieceType.ROOK: "R",
    PieceType.QUEEN: "Q",
    PieceType.KING: "K",
}
