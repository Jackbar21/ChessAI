"""
Board representation and game state management.
"""

from typing import List, Optional, Tuple, Dict, Any
from src.constants import Color, PieceType
from src.piece import Piece
from src.move import Move
from src.game_state import GameState, CastlingRights


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

        # Game state - using proper GameState dataclass
        self.game_state = GameState()
        
        # Move history for unmake_move (move, game_state, captured_piece_info)
        self.move_history: List[Tuple[Move, GameState, Optional[Tuple[int, int, Piece]]]] = []
    
    # Properties for backward compatibility and convenience
    @property
    def turn(self) -> Color:
        """Get current turn."""
        return self.game_state.turn
    
    @turn.setter
    def turn(self, value: Color) -> None:
        """Set current turn."""
        self.game_state.turn = value
    
    @property
    def en_passant_square(self) -> Optional[Tuple[int, int]]:
        """Get en passant square."""
        return self.game_state.en_passant_square
    
    @en_passant_square.setter
    def en_passant_square(self, value: Optional[Tuple[int, int]]) -> None:
        """Set en passant square."""
        self.game_state.en_passant_square = value
    
    @property
    def halfmove_clock(self) -> int:
        """Get halfmove clock."""
        return self.game_state.halfmove_clock
    
    @halfmove_clock.setter
    def halfmove_clock(self, value: int) -> None:
        """Set halfmove clock."""
        self.game_state.halfmove_clock = value
    
    @property
    def fullmove_number(self) -> int:
        """Get fullmove number."""
        return self.game_state.fullmove_number
    
    @fullmove_number.setter
    def fullmove_number(self, value: int) -> None:
        """Set fullmove number."""
        self.game_state.fullmove_number = value
    
    @property
    def castling_rights(self) -> CastlingRights:
        """Get castling rights."""
        return self.game_state.castling_rights

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

        # Reset game state to initial position
        self.game_state = GameState()  # Creates fresh state with defaults
        
        # Clear move history
        self.move_history = []

    def opponent_color(self) -> Color:
        """Get the opponent's color."""
        return Color.BLACK if self.turn == Color.WHITE else Color.WHITE

    def find_king(self, color: Color) -> Optional[Tuple[int, int]]:
        """
        Find the position of the king for the given color.

        Args:
            color: The color of the king to find

        Returns:
            (rank, file) tuple of king position, or None if not found
        """
        pieces = self.white_pieces if color == Color.WHITE else self.black_pieces
        for rank, file, piece in pieces:
            if piece.piece_type == PieceType.KING:
                return (rank, file)
        raise ValueError("King must be on the board")

    def is_square_attacked(self, rank: int, file: int, by_color: Color) -> bool:
        """
        Check if a square is attacked by the given color.

        Args:
            rank: The rank of the square to check
            file: The file of the square to check
            by_color: The color attacking the square

        Returns:
            True if the square is attacked, False otherwise
        """
        # Check for pawn attacks
        pawn_direction = -1 if by_color == Color.WHITE else 1
        for df in [-1, 1]:
            pawn_rank = rank - pawn_direction
            pawn_file = file + df
            if 0 <= pawn_rank < 8 and 0 <= pawn_file < 8:
                piece = self.get_piece(pawn_rank, pawn_file)
                if (
                    piece
                    and piece.color == by_color
                    and piece.piece_type == PieceType.PAWN
                ):
                    return True

        # Check for knight attacks
        knight_offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        for dr, df in knight_offsets:
            new_rank = rank + dr
            new_file = file + df
            if 0 <= new_rank < 8 and 0 <= new_file < 8:
                piece = self.get_piece(new_rank, new_file)
                if (
                    piece
                    and piece.color == by_color
                    and piece.piece_type == PieceType.KNIGHT
                ):
                    return True

        # Check for sliding piece attacks (bishop, rook, queen)
        # Diagonal directions (bishop and queen)
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, df in diagonal_directions:
            new_rank = rank + dr
            new_file = file + df
            while 0 <= new_rank < 8 and 0 <= new_file < 8:
                piece = self.get_piece(new_rank, new_file)
                if piece:
                    if piece.color == by_color and piece.piece_type in [
                        PieceType.BISHOP,
                        PieceType.QUEEN,
                    ]:
                        return True
                    break  # Blocked by any piece
                new_rank += dr
                new_file += df

        # Orthogonal directions (rook and queen)
        orthogonal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, df in orthogonal_directions:
            new_rank = rank + dr
            new_file = file + df
            while 0 <= new_rank < 8 and 0 <= new_file < 8:
                piece = self.get_piece(new_rank, new_file)
                if piece:
                    if piece.color == by_color and piece.piece_type in [
                        PieceType.ROOK,
                        PieceType.QUEEN,
                    ]:
                        return True
                    break
                new_rank += dr
                new_file += df

        # Check for king attacks
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                if dr == 0 and df == 0:
                    continue
                new_rank = rank + dr
                new_file = file + df
                if 0 <= new_rank < 8 and 0 <= new_file < 8:
                    piece = self.get_piece(new_rank, new_file)
                    if (
                        piece
                        and piece.color == by_color
                        and piece.piece_type == PieceType.KING
                    ):
                        return True

        return False

    def is_in_check(self, color: Color) -> bool:
        """
        Check if the given color's king is in check.

        Args:
            color: The color to check

        Returns:
            True if the king is in check, False otherwise
        """
        king_rank, king_file = self.find_king(color)

        # Check if attacked by the opposite color
        attacker_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        return self.is_square_attacked(king_rank, king_file, attacker_color)

    def make_move(self, move: Move) -> None:
        """
        Make a move on the board.

        Args:
            move: The move to make
        """
        # Save complete game state for unmake_move  
        saved_state = self.game_state.copy()
        
        # Track captured piece separately (board state, not game state)
        captured_piece_info: Optional[Tuple[int, int, Piece]] = None

        moving_piece = self.get_piece(move.from_rank, move.from_file)
        if moving_piece is None:
            raise ValueError(f"No piece at {move.from_rank},{move.from_file}")

        # Handle captures
        if move.is_en_passant:
            # Remove the captured pawn
            capture_rank = move.to_rank - (
                1 if moving_piece.color == Color.WHITE else -1
            )
            captured_piece = self.get_piece(capture_rank, move.to_file)
            assert captured_piece.piece_type == PieceType.PAWN
            captured_piece_info = (capture_rank, move.to_file, captured_piece)
            self.set_piece(capture_rank, move.to_file, None)
            self.halfmove_clock = 0
        elif move.captured_piece_type:
            captured_piece = self.get_piece(move.to_rank, move.to_file)
            captured_piece_info = (move.to_rank, move.to_file, captured_piece)
            self.halfmove_clock = 0
        elif moving_piece.piece_type == PieceType.PAWN:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # Move the piece
        self.set_piece(move.from_rank, move.from_file, None)

        # Handle promotion
        if move.promotion_piece_type:
            promoted_piece = Piece(move.promotion_piece_type, moving_piece.color)
            self.set_piece(move.to_rank, move.to_file, promoted_piece)
        else:
            self.set_piece(move.to_rank, move.to_file, moving_piece)

        # Handle castling
        if move.is_castling:
            # Move the rook
            if move.to_file == 6:  # Kingside
                rook = self.get_piece(move.from_rank, 7)
                assert rook and rook.piece_type == PieceType.ROOK
                assert self.get_piece(move.from_rank, 5) is None
                self.set_piece(move.from_rank, 7, None)
                self.set_piece(move.from_rank, 5, rook)
            else:  # Queenside (to_file == 2)
                rook = self.get_piece(move.from_rank, 0)
                assert rook and rook.piece_type == PieceType.ROOK
                assert self.get_piece(move.from_rank, 3) is None
                self.set_piece(move.from_rank, 0, None)
                self.set_piece(move.from_rank, 3, rook)

        # Update en passant square
        if (
            moving_piece.piece_type == PieceType.PAWN
            and abs(move.to_rank - move.from_rank) == 2
        ):
            # Double pawn push - set en passant square
            self.en_passant_square = (
                (move.from_rank + move.to_rank) // 2,
                move.from_file,
            )
        else:
            self.en_passant_square = None

        # Update castling rights using new CastlingRights API
        if moving_piece.piece_type == PieceType.KING:
            self.castling_rights.revoke_all(moving_piece.color)
        elif moving_piece.piece_type == PieceType.ROOK:
            if move.from_file == 0:  # Queenside rook
                self.castling_rights.set_queenside(moving_piece.color, False)
            elif move.from_file == 7:  # Kingside rook
                self.castling_rights.set_kingside(moving_piece.color, False)

        # If a rook is captured, update opponent's castling rights
        if move.captured_piece_type == PieceType.ROOK:
            opponent = self.opponent_color()
            if move.to_file == 0 and move.to_rank == (
                0 if opponent == Color.WHITE else 7
            ):
                self.castling_rights.set_queenside(opponent, False)
            elif move.to_file == 7 and move.to_rank == (
                0 if opponent == Color.WHITE else 7
            ):
                self.castling_rights.set_kingside(opponent, False)

        # Update turn
        if self.turn == Color.BLACK:
            self.fullmove_number += 1
        self.turn = self.opponent_color()

        # Save to history with both saved_state and captured_piece_info
        # We need to store captured piece info separately since it's board state
        self.move_history.append((move, saved_state, captured_piece_info))

    def unmake_move(self) -> None:
        """Unmake the last move."""
        if not self.move_history:
            raise ValueError("No moves to unmake")

        move, saved_state, captured_piece_info = self.move_history.pop()

        # Restore game state
        self.game_state = saved_state

        # Get the piece that was moved (it's now at the destination)
        moving_piece = self.get_piece(move.to_rank, move.to_file)
        if moving_piece is None:
            raise ValueError(f"No piece at destination {move.to_rank},{move.to_file}")

        # Handle promotion - restore to pawn
        if move.promotion_piece_type:
            moving_piece = Piece(PieceType.PAWN, moving_piece.color)

        # Move piece back
        self.set_piece(move.to_rank, move.to_file, None)
        self.set_piece(move.from_rank, move.from_file, moving_piece)

        # Restore captured piece
        if captured_piece_info:
            cap_rank, cap_file, captured_piece = captured_piece_info
            self.set_piece(cap_rank, cap_file, captured_piece)

        # Undo castling rook move
        if move.is_castling:
            if move.to_file == 6:  # Kingside
                rook = self.get_piece(move.from_rank, 5)
                assert rook and rook.piece_type == PieceType.ROOK
                assert self.get_piece(move.from_rank, 7) is None
                self.set_piece(move.from_rank, 5, None)
                self.set_piece(move.from_rank, 7, rook)
            else:  # Queenside
                rook = self.get_piece(move.from_rank, 3)
                assert rook and rook.piece_type == PieceType.ROOK
                assert self.get_piece(move.from_rank, 0) is None
                self.set_piece(move.from_rank, 3, None)
                self.set_piece(move.from_rank, 0, rook)
