"""
Move representation for the chess engine.
"""

from typing import Optional
from src.constants import PieceType, PIECE_CHARS


class Move:
    """
    Represents a chess move.

    Stores all information needed to make and unmake moves.
    """

    def __init__(
        self,
        from_rank: int,
        from_file: int,
        to_rank: int,
        to_file: int,
        captured_piece_type: Optional[PieceType] = None,
        is_en_passant: bool = False,
        is_castling: bool = False,
        promotion_piece_type: Optional[PieceType] = None,
    ):
        """
        Initialize a move.

        Args:
            from_rank: Starting rank (0-7)
            from_file: Starting file (0-7)
            to_rank: Destination rank (0-7)
            to_file: Destination file (0-7)
            captured_piece_type: Type of piece captured, if any
            is_en_passant: True if this is an en passant capture
            is_castling: True if this is a castling move
            promotion_piece_type: Piece type to promote to, if any
        """
        self.from_rank = from_rank
        self.from_file = from_file
        self.to_rank = to_rank
        self.to_file = to_file
        self.captured_piece_type = captured_piece_type
        self.is_en_passant = is_en_passant
        self.is_castling = is_castling
        self.promotion_piece_type = promotion_piece_type
    def __repr__(self):
        """String representation of the move."""
        from_sq = self._square_to_notation(self.from_rank, self.from_file)
        to_sq = self._square_to_notation(self.to_rank, self.to_file)
        result = f"{from_sq}{to_sq}"

        if self.promotion_piece_type:
            assert self.promotion_piece_type in (
                PieceType.KNIGHT,
                PieceType.BISHOP,
                PieceType.ROOK,
                PieceType.QUEEN,
            ), "Invalid promotion piece type"
            result += PIECE_CHARS[self.promotion_piece_type].lower()

        return result

    def __str__(self):
        """Human-readable string representation."""
        from_sq = self._square_to_notation(self.from_rank, self.from_file)
        to_sq = self._square_to_notation(self.to_rank, self.to_file)

        result = f"{from_sq} -> {to_sq}"

        if self.is_castling:
            result += " (castling)"
        elif self.is_en_passant:
            result += " (en passant)"
        elif self.captured_piece_type:
            result += f" (captures {self.captured_piece_type.name})"

        if self.promotion_piece_type:
            result += f" (promotes to {self.promotion_piece_type.name})"

        return result

    def __eq__(self, other):
        """Check if two moves are equal."""
        if not isinstance(other, Move):
            return False
        return (
            self.from_rank == other.from_rank
            and self.from_file == other.from_file
            and self.to_rank == other.to_rank
            and self.to_file == other.to_file
            and self.promotion_piece_type == other.promotion_piece_type
            and self.is_en_passant == other.is_en_passant
            and self.is_castling == other.is_castling
            and self.captured_piece_type == other.captured_piece_type
        )

    def __hash__(self):
        """Make Move hashable for use in sets and dicts."""
        return hash(
            (
                self.from_rank,
                self.from_file,
                self.to_rank,
                self.to_file,
                self.promotion_piece_type,
                self.is_en_passant,
                self.is_castling,
                self.captured_piece_type,
            )
        )

    @staticmethod
    def _square_to_notation(rank: int, file: int) -> str:
        """Convert rank/file to algebraic notation."""
        assert (
            0 <= rank <= 7 and 0 <= file <= 7
        ), "Rank and file must be between 0 and 7"
        return f"{'abcdefgh'[file]}{rank + 1}"
