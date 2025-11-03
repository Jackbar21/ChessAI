"""
Piece representation for the chess engine.
"""

from src.core.constants import Color, PieceType


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
        self.color = color
        self.piece_type = piece_type
        self.id = piece_type.id
        self.centipawn_value = piece_type.centipawn_value
        self.char = piece_type.char

    def __repr__(self):
        """String representation of the piece."""
        return f"{self.color.name} {self.piece_type.name}"

    def __str__(self):
        """
        Returns a single character representation for board display.
        Uppercase for white, lowercase for black.
        """
        return self.char if self.color == Color.WHITE else self.char.lower()

    def __hash__(self):
        """
        Make Piece hashable for use in sets.
        Two pieces are considered the same if they have the same type and color.
        Note: This does not consider position, this is handled by the Board.
        """
        return hash((self.piece_type, self.color))

    def __eq__(self, other):
        """
        Check equality based on piece type and color.
        Note: This does not consider position, this is handled by the Board.
        """
        if not isinstance(other, Piece):
            return False
        return self.piece_type == other.piece_type and self.color == other.color
