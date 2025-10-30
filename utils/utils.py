from src.move import Move
from src.constants import PieceType


def _verify_square(notation: str) -> None:
    """Helper to verify square notation."""
    assert len(notation) == 2, "Invalid square notation"
    assert notation[0] in "abcdefgh", "Invalid file"
    assert notation[1] in "12345678", "Invalid rank"


def get_rank_file(notation: str) -> tuple[int, int]:
    """Convert algebraic notation (e.g., 'e4') to (rank, file) tuple."""
    _verify_square(notation)

    file_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    file = file_map[notation[0]]
    rank = int(notation[1]) - 1
    return rank, file


def get_move(from_sq: str, to_sq: str, promotion: PieceType = None) -> Move:
    """Helper to create a Move from algebraic notation."""

    from_rank, from_file = get_rank_file(from_sq)
    to_rank, to_file = get_rank_file(to_sq)
    return Move(from_rank, from_file, to_rank, to_file, promotion_piece_type=promotion)
