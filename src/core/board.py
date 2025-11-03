"""
Board representation and game state management.
"""

from typing import List, Optional, Tuple, Dict, Any
from src.core.constants import Color, PieceType, GameStatus
from src.core.piece import Piece
from src.core.move import Move
from collections import defaultdict


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
        self.major_minor_count = (
            0  # Major/minor piece count (excluding kings and pawns)
        )

        # Game state
        self.turn = Color.WHITE
        self.en_passant_square: Optional[Tuple[int, int]] = None
        self.castling_rights = {
            Color.WHITE: {"kingside": True, "queenside": True},
            Color.BLACK: {"kingside": True, "queenside": True},
        }
        self.halfmove_clock = 0  # For 50-move rule
        self.fullmove_number = 1
        self.fen_history: Dict[str, int] = defaultdict(int)  # For threefold repetition

        # Move history for unmake_move
        self.move_history: List[Tuple[Move, Dict[str, Any]]] = []

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
            if old_piece.piece_type not in (PieceType.KING, PieceType.PAWN):
                self.major_minor_count -= 1

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
            if piece.piece_type not in (PieceType.KING, PieceType.PAWN):
                self.major_minor_count += 1

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

    def __str__(self) -> str:
        """String representation of the board."""
        # TODO: Change to FEN, for now used for local debugging
        return self.display()

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
            pawn_rank = rank + pawn_direction
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

    def is_insufficient_material(self) -> bool:
        """
        Check for insufficient material to continue the game.

        Returns:
            True if insufficient material, False otherwise
        """
        # All pieces except kings
        pieces = [
            (rank, file, piece)
            for rank, file, piece in list(self.white_pieces) + list(self.black_pieces)
            if piece.piece_type != PieceType.KING
        ]

        # King vs King
        if len(pieces) == 0:
            return True

        # King vs King and Bishop/Knight
        if len(pieces) == 1:
            _, _, piece = pieces[0]
            if piece.piece_type in [PieceType.BISHOP, PieceType.KNIGHT]:
                return True

        # King and Bishop vs King and Bishop (same color bishops)
        if len(pieces) == 2:
            rank1, file1, piece1 = pieces[0]
            rank2, file2, piece2 = pieces[1]
            if (
                piece1.piece_type == PieceType.BISHOP
                and piece2.piece_type == PieceType.BISHOP
            ):
                square_color1 = (rank1 + file1) % 2
                square_color2 = (rank2 + file2) % 2
                if square_color1 == square_color2:
                    return True

        return False

    def is_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns:
            True if the game is over, False otherwise
        """
        result = self.get_game_status()
        return result != GameStatus.ONGOING

    def is_technical_draw(self) -> bool:
        """
        Check if the game is a technical draw via one of the following:
        1. 50-move rule
        2. Threefold repetition
        3. Insufficient material
        """
        # 50-move rule
        if self.halfmove_clock >= 100:
            return True

        # Threefold repetition
        if self.fen_history[self.position_fen()] >= 3:
            return True
        else:
            assert max(self.fen_history.values(), default=0) < 3  # Sanity check

        # Insufficient material
        if self.is_insufficient_material():
            return True

        return False

    def get_game_status(self) -> GameStatus:
        """
        Get the status of the game.

        Returns:
            GameResult enum indicating the game status
        """
        # Check for 50-move rule, threefold repetition, insufficient material
        if self.is_technical_draw():
            return GameStatus.DRAW

        from src.core.movegen import MoveGenerator

        move_gen = MoveGenerator(self)

        # No legal moves (checkmate or stalemate)
        legal_moves = list(move_gen.generate_legal_moves())
        if not legal_moves:
            # Checkmate
            if self.is_in_check(self.turn):
                return (
                    GameStatus.BLACK_WON
                    if self.turn == Color.WHITE
                    else GameStatus.WHITE_WON
                )
            # Stalemate
            else:
                assert not self.is_in_check(self.opponent_color())
                return GameStatus.DRAW

        # Game is not over
        return GameStatus.ONGOING

    def make_move(self, move: Move) -> None:
        """
        Make a move on the board.

        Args:
            move: The move to make
        """
        # Save state for unmake_move
        state = {
            "en_passant_square": self.en_passant_square,
            "castling_rights": {
                Color.WHITE: self.castling_rights[Color.WHITE].copy(),
                Color.BLACK: self.castling_rights[Color.BLACK].copy(),
            },
            "halfmove_clock": self.halfmove_clock,
            "fullmove_number": self.fullmove_number,
            "captured_piece": None,
        }

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
            state["captured_piece"] = (capture_rank, move.to_file, captured_piece)
            self.set_piece(capture_rank, move.to_file, None)
            self.halfmove_clock = 0
        elif move.captured_piece_type:
            captured_piece = self.get_piece(move.to_rank, move.to_file)
            state["captured_piece"] = (move.to_rank, move.to_file, captured_piece)
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

        # Update castling rights
        if moving_piece.piece_type == PieceType.KING:
            self.castling_rights[moving_piece.color]["kingside"] = False
            self.castling_rights[moving_piece.color]["queenside"] = False
        elif moving_piece.piece_type == PieceType.ROOK:
            if move.from_file == 0:  # Queenside rook
                self.castling_rights[moving_piece.color]["queenside"] = False
            elif move.from_file == 7:  # Kingside rook
                self.castling_rights[moving_piece.color]["kingside"] = False

        # If a rook is captured, update opponent's castling rights
        if move.captured_piece_type == PieceType.ROOK:
            opponent = self.opponent_color()
            if move.to_file == 0 and move.to_rank == (
                0 if opponent == Color.WHITE else 7
            ):
                self.castling_rights[opponent]["queenside"] = False
            elif move.to_file == 7 and move.to_rank == (
                0 if opponent == Color.WHITE else 7
            ):
                self.castling_rights[opponent]["kingside"] = False

        # Update turn
        if self.turn == Color.BLACK:
            self.fullmove_number += 1
        self.turn = self.opponent_color()

        # Save to history
        self.move_history.append((move, state))
        self.fen_history[self.position_fen()] += 1

    def unmake_move(self) -> None:
        """Unmake the last move."""
        if not self.move_history:
            raise ValueError("No moves to unmake")

        # Decrement FEN history
        position_fen = self.position_fen()
        self.fen_history[position_fen] -= 1
        assert self.fen_history[position_fen] >= 0
        move, state = self.move_history.pop()

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
        if state["captured_piece"]:
            cap_rank, cap_file, captured_piece = state["captured_piece"]
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

        # Restore game state
        self.turn = self.opponent_color()
        self.en_passant_square = state["en_passant_square"]
        self.castling_rights = state["castling_rights"]
        self.halfmove_clock = state["halfmove_clock"]
        self.fullmove_number = state["fullmove_number"]

    def to_fen(self) -> str:
        """
        Convert the current board position to FEN notation.

        Returns:
            FEN string representing the current position
        """
        fen_parts = []

        # Piece placement
        for rank in range(7, -1, -1):
            empty_count = 0
            rank_fen = ""
            for file in range(8):
                piece = self.get_piece(rank, file)
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        rank_fen += str(empty_count)
                        empty_count = 0
                    rank_fen += str(piece)
            if empty_count > 0:
                rank_fen += str(empty_count)
            fen_parts.append(rank_fen)
        fen_position = "/".join(fen_parts)

        # Active color
        fen_active_color = "w" if self.turn == Color.WHITE else "b"

        # Castling rights
        castling = ""
        if self.castling_rights[Color.WHITE]["kingside"]:
            castling += "K"
        if self.castling_rights[Color.WHITE]["queenside"]:
            castling += "Q"
        if self.castling_rights[Color.BLACK]["kingside"]:
            castling += "k"
        if self.castling_rights[Color.BLACK]["queenside"]:
            castling += "q"
        if castling == "":
            castling = "-"

        # En passant target square
        if self.en_passant_square:
            ep_square = self.square_to_notation(
                self.en_passant_square[0], self.en_passant_square[1]
            )
        else:
            ep_square = "-"

        # Halfmove clock and fullmove number
        fen_halfmove = str(self.halfmove_clock)
        fen_fullmove = str(self.fullmove_number)

        # Combine all parts
        fen = f"{fen_position} {fen_active_color} {castling} {ep_square} {fen_halfmove} {fen_fullmove}"
        return fen

    def position_fen_from_fen(self, fen: str) -> str:
        """
        Get the position FEN from a full FEN string.

        Args:
            fen: The full FEN string
        Returns:
            Position FEN string
        """
        rows, color, castling, ep_square, _, _ = fen.split()
        return " ".join([rows, color, castling, ep_square])  # ignore halfmove/fullmove

    def position_fen(self) -> str:
        """
        FEN string suitable for repetition detection:
        ignores halfmove clock and fullmove number.
        """
        full_fen = self.to_fen()
        return self.position_fen_from_fen(full_fen)

    def from_fen(self, fen: str) -> None:
        """
        Set up the board from a FEN string.

        Args:
            fen: The FEN string to set up the board
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_pieces = set()
        self.black_pieces = set()

        rows, color, castling, ep_square, halfmove, fullmove = fen.split()
        self.turn = Color.WHITE if color == "w" else Color.BLACK
        self.en_passant_square = (
            self.notation_to_square(ep_square) if ep_square != "-" else None
        )
        self.castling_rights = {
            Color.WHITE: {"kingside": "K" in castling, "queenside": "Q" in castling},
            Color.BLACK: {"kingside": "k" in castling, "queenside": "q" in castling},
        }
        self.halfmove_clock = int(halfmove)
        self.fullmove_number = int(fullmove)

        # Unfortunately, fen_history and move_history cannot be reconstructed from FEN
        self.fen_history = defaultdict(int)
        self.fen_history[self.position_fen_from_fen(fen)] = 1  # Current position
        self.move_history = []

        rows = rows.split("/")
        for rank in range(8):
            file = 0
            for char in rows[rank]:
                if char.isdigit():
                    file += int(char)
                else:
                    piece_color = Color.WHITE if char.isupper() else Color.BLACK
                    # Build a reverse lookup from char to PieceType
                    fen_char_to_piece_type = {pt.char.upper(): pt for pt in PieceType}
                    piece_type = fen_char_to_piece_type[char.upper()]
                    piece = Piece(piece_type, piece_color)
                    self.set_piece(7 - rank, file, piece)
                    file += 1

    def setup_initial_position(self) -> None:
        """Set up the standard chess starting position."""
        initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.from_fen(initial_fen)

    def get_move_from_uci(self, uci: str) -> Move:
        """
        Convert a UCI string to a Move object.

        Args:
            uci: The UCI string (e.g., 'e2e4', 'e7e8q')

        Returns:
            The corresponding Move object
        """
        from_file = "abcdefgh".index(uci[0])
        from_rank = int(uci[1]) - 1
        to_file = "abcdefgh".index(uci[2])
        to_rank = int(uci[3]) - 1

        promotion_piece_type = None
        if len(uci) == 5:
            promotion_char = uci[4].upper()
            fen_char_to_piece_type = {pt.char.upper(): pt for pt in PieceType}
            promotion_piece_type = fen_char_to_piece_type[promotion_char]

        moving_piece = self.get_piece(from_rank, from_file)
        if moving_piece is None:
            raise ValueError(f"No piece at {from_rank},{from_file}")

        captured_piece_type = None
        is_en_passant = (
            moving_piece.piece_type == PieceType.PAWN
            and (to_rank, to_file) == self.en_passant_square
        )
        if is_en_passant:
            captured_piece_type = PieceType.PAWN
        elif self.get_piece(to_rank, to_file):
            captured_piece_type = self.get_piece(to_rank, to_file).piece_type

        is_castling = (
            moving_piece.piece_type == PieceType.KING
            and abs(to_rank - from_rank) == 0
            and abs(to_file - from_file) == 2
        )

        return Move(
            from_rank=from_rank,
            from_file=from_file,
            to_rank=to_rank,
            to_file=to_file,
            captured_piece_type=captured_piece_type,
            is_en_passant=is_en_passant,
            is_castling=is_castling,
            promotion_piece_type=promotion_piece_type,
        )
