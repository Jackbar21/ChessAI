"""
Piece representation for the chess engine.
"""

from src.constants import Color, PieceType, PIECE_VALUES, PIECE_CHARS


class Piece:
    """
    Represents a chess piece.

    Note: Pieces don't store their position - the Board keeps track of that.
    This makes move generation and board updates simpler.
    """

    def __init__(self, piece_type: PieceType, color: Color):
        """
        Initialize a chess piece.

        Args:
            piece_type: The type of piece (PAWN, KNIGHT, etc.)
            color: The color of the piece (WHITE or BLACK)
        """
        self.piece_type = piece_type
        self.color = color
        self.value = PIECE_VALUES[piece_type]
        self.char = PIECE_CHARS[piece_type]

    def __repr__(self):
        """String representation of the piece."""
        return f"{self.color.name} {self.piece_type.name}"

    def __str__(self):
        """
        Returns a single character representation for board display.
        Uppercase for white, lowercase for black.
        """
        return self.char if self.color == Color.WHITE else self.char.lower()
