"""
Board representation and game state management.
"""

from typing import List, Optional, Tuple
from src.constants import Color, PieceType
from src.piece import Piece


class Board:
    """
    Represents the chess board using an 8x8 array.

    Board indexing: board[rank][file]
    - rank 0 = rank 1 (white's back rank)
    - rank 7 = rank 8 (black's back rank)
    - file 0 = a-file, file 7 = h-file

    So board[0][0] = A1, board[7][7] = H8
    """

    def __init__(self):
        """Initialize an empty chess board."""
        # 8x8 array, None represents empty squares
        self.board: List[List[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

        # Keep track of pieces for easy iteration
        self.white_pieces: set[Tuple[int, int, Piece]] = set()  # (rank, file, piece)
        self.black_pieces: set[Tuple[int, int, Piece]] = set()  # (rank, file, piece)

        # Game state
        self.turn = Color.WHITE
        self.en_passant_square: Optional[Tuple[int, int]] = None
        self.castling_rights = {
            Color.WHITE: {"kingside": True, "queenside": True},
            Color.BLACK: {"kingside": True, "queenside": True},
        }
        self.halfmove_clock = 0  # For 50-move rule
        self.fullmove_number = 1

    def get_piece(self, rank: int, file: int) -> Optional[Piece]:
        """
        Get the piece at a specific square.

        Args:
            rank: The rank (0-7, where 0 is rank 1)
            file: The file (0-7, where 0 is a-file)

        Returns:
            The piece at that square, or None if empty
        """
        if not (0 <= rank < 8 and 0 <= file < 8):
            return None
        return self.board[rank][file]

    def set_piece(self, rank: int, file: int, piece: Optional[Piece]) -> None:
        """
        Set a piece at a specific square.

        Args:
            rank: The rank (0-7)
            file: The file (0-7)
            piece: The piece to place, or None to clear the square
        """
        # Remove old piece from piece lists if it exists (get rekt)
        old_piece = self.board[rank][file]
        if old_piece:
            piece_set = (
                self.white_pieces
                if old_piece.color == Color.WHITE
                else self.black_pieces
            )
            # Using set remove instead of discard to catch errors
            piece_set.remove((rank, file, old_piece))

        # Set the new piece
        self.board[rank][file] = piece

        # Add new piece to piece lists if it exists
        if piece:
            if piece.color == Color.WHITE:
                assert (rank, file, piece) not in self.white_pieces
                self.white_pieces.add((rank, file, piece))
            else:
                assert (rank, file, piece) not in self.black_pieces
                self.black_pieces.add((rank, file, piece))

    def square_to_notation(self, rank: int, file: int) -> str:
        """Convert rank/file to algebraic notation (e.g., 0,0 -> 'a1')."""
        return f"{'abcdefgh'[file]}{rank + 1}"

    def notation_to_square(self, notation: str) -> Tuple[int, int]:
        """Convert algebraic notation to rank/file (e.g., 'a1' -> 0,0)."""
        file = "abcdefgh".index(notation[0].lower())
        rank = int(notation[1]) - 1
        return rank, file

    def display(self) -> str:
        """
        Return a string representation of the board for display.
        """
        lines = []
        lines.append("  +---+---+---+---+---+---+---+---+")

        # Display from rank 7 to rank 0 (8 to 1)
        for rank in range(7, -1, -1):
            line = f"{rank + 1} |"
            for file in range(8):
                piece = self.board[rank][file]
                if piece:
                    line += f" {str(piece)} |"
                else:
                    line += "   |"
            lines.append(line)
            lines.append("  +---+---+---+---+---+---+---+---+")

        lines.append("    a   b   c   d   e   f   g   h")
        return "\n".join(lines)

    def evaluate(self) -> int:
        """
        Simple material evaluation.
        Positive score favors white, negative favors black.

        Returns:
            Evaluation score in centipawns
        """
        score = 0
        for rank in range(8):
            for file in range(8):
                piece = self.board[rank][file]
                if piece:
                    value = piece.value
                    if piece.color == Color.WHITE:
                        score += value
                    else:
                        score -= value
        return score

    def setup_initial_position(self) -> None:
        """Set up the standard chess starting position."""
        # Clear the board
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_pieces = set()
        self.black_pieces = set()

        # White pieces (rank 0)
        self.set_piece(0, 0, Piece(PieceType.ROOK, Color.WHITE))
        self.set_piece(0, 1, Piece(PieceType.KNIGHT, Color.WHITE))
        self.set_piece(0, 2, Piece(PieceType.BISHOP, Color.WHITE))
        self.set_piece(0, 3, Piece(PieceType.QUEEN, Color.WHITE))
        self.set_piece(0, 4, Piece(PieceType.KING, Color.WHITE))
        self.set_piece(0, 5, Piece(PieceType.BISHOP, Color.WHITE))
        self.set_piece(0, 6, Piece(PieceType.KNIGHT, Color.WHITE))
        self.set_piece(0, 7, Piece(PieceType.ROOK, Color.WHITE))

        # White pawns (rank 1)
        for file in range(8):
            self.set_piece(1, file, Piece(PieceType.PAWN, Color.WHITE))

        # Black pieces (rank 7)
        self.set_piece(7, 0, Piece(PieceType.ROOK, Color.BLACK))
        self.set_piece(7, 1, Piece(PieceType.KNIGHT, Color.BLACK))
        self.set_piece(7, 2, Piece(PieceType.BISHOP, Color.BLACK))
        self.set_piece(7, 3, Piece(PieceType.QUEEN, Color.BLACK))
        self.set_piece(7, 4, Piece(PieceType.KING, Color.BLACK))
        self.set_piece(7, 5, Piece(PieceType.BISHOP, Color.BLACK))
        self.set_piece(7, 6, Piece(PieceType.KNIGHT, Color.BLACK))
        self.set_piece(7, 7, Piece(PieceType.ROOK, Color.BLACK))

        # Black pawns (rank 6)
        for file in range(8):
            self.set_piece(6, file, Piece(PieceType.PAWN, Color.BLACK))

        # Reset game state
        self.turn = Color.WHITE
        self.en_passant_square = None
        self.castling_rights = {
            Color.WHITE: {"kingside": True, "queenside": True},
            Color.BLACK: {"kingside": True, "queenside": True},
        }
        self.halfmove_clock = 0
        self.fullmove_number = 1
