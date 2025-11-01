"""
Move representation for the chess engine.
"""

from typing import Optional
from src.constants import PieceType


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
        return self.to_uci()

    def _square_to_notation(self, rank: int, file: int) -> str:
        """Convert rank/file to algebraic notation (e.g., 0,0 -> 'a1')."""
        return f"{'abcdefgh'[file]}{rank + 1}"

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

    def to_uci(self) -> str:
        """Convert the move to UCI format (e.g., 'e2e4', 'e7e8q')."""
        from_sq = self._square_to_notation(self.from_rank, self.from_file)
        to_sq = self._square_to_notation(self.to_rank, self.to_file)
        uci_move = f"{from_sq}{to_sq}"

        if self.promotion_piece_type:
            assert (
                self.promotion_piece_type.is_promotable
            ), "Invalid promotion piece type"
            uci_move += self.promotion_piece_type.char.lower()

        return uci_move

    @staticmethod
    def from_uci(uci_str: str) -> Optional["Move"]:
        """Create a Move object from a UCI format string."""
        if not (4 <= len(uci_str) <= 5):
            return None

        try:
            from_file = ord(uci_str[0]) - ord("a")
            from_rank = int(uci_str[1]) - 1
            to_file = ord(uci_str[2]) - ord("a")
            to_rank = int(uci_str[3]) - 1

            promotion_type = None
            if len(uci_str) == 5:
                promotion_char = uci_str[4].lower()
                promotion_map = {
                    "q": PieceType.QUEEN,
                    "r": PieceType.ROOK,
                    "b": PieceType.BISHOP,
                    "n": PieceType.KNIGHT,
                }
                promotion_type = promotion_map[promotion_char]

            return Move(
                from_rank,
                from_file,
                to_rank,
                to_file,
                promotion_piece_type=promotion_type,
            )

        except (ValueError, IndexError):
            return None
