"""
Move generation for the chess engine.

This module handles generating all legal moves for each piece type,
including special moves like castling, en passant, and pawn promotion.
"""

from typing import List, Tuple
from src.constants import Color, PieceType
from src.move import Move
from src.board import Board


class MoveGenerator:
    """Generates legal moves for a chess position."""

    def __init__(self, board: Board):
        """
        Initialize the move generator.

        Args:
            board: The Board instance to generate moves for
        """
        self.board = board

    def generate_legal_moves(self) -> List[Move]:
        """
        Generate all legal moves for the current position.

        Returns:
            List of legal Move objects
        """
        pseudo_legal_moves = self.generate_pseudo_legal_moves()
        legal_moves = []

        # Filter out moves that leave the king in check
        for move in pseudo_legal_moves:
            if self._is_legal(move):
                legal_moves.append(move)

        return legal_moves

    def generate_pseudo_legal_moves(self) -> List[Move]:
        """
        Generate all pseudo-legal moves (moves that follow piece movement rules
        but may leave the king in check).

        Returns:
            List of pseudo-legal Move objects
        """
        moves = []
        current_color = self.board.turn

        # Get pieces for the current player
        pieces = (
            self.board.white_pieces
            if current_color == Color.WHITE
            else self.board.black_pieces
        )

        move_generators = {
            PieceType.PAWN: self._generate_pawn_moves,
            PieceType.KNIGHT: self._generate_knight_moves,
            PieceType.BISHOP: self._generate_bishop_moves,
            PieceType.ROOK: self._generate_rook_moves,
            PieceType.QUEEN: self._generate_queen_moves,
            PieceType.KING: self._generate_king_moves,
        }
        for rank, file, piece in pieces:
            generator = move_generators.get(piece.piece_type)
            assert generator is not None  # Should never be None
            moves.extend(generator(rank, file, piece))
        return moves

    def _generate_pawn_moves(self, rank: int, file: int, piece) -> List[Move]:
        """Generate all pawn moves from the given position."""
        moves = []
        direction = 1 if piece.color == Color.WHITE else -1
        start_rank = 1 if piece.color == Color.WHITE else 6
        promotion_rank = 7 if piece.color == Color.WHITE else 0

        # Single push
        new_rank = rank + direction
        if 0 <= new_rank < 8 and self.board.get_piece(new_rank, file) is None:
            # Check for promotion
            if new_rank == promotion_rank:
                for promo_type in [
                    PieceType.QUEEN,
                    PieceType.ROOK,
                    PieceType.BISHOP,
                    PieceType.KNIGHT,
                ]:
                    moves.append(
                        Move(
                            rank, file, new_rank, file, promotion_piece_type=promo_type
                        )
                    )
            else:
                moves.append(Move(rank, file, new_rank, file))

            # Double push from starting position
            if rank == start_rank:
                single_rank = rank + direction
                double_rank = rank + 2 * direction
                if (
                    self.board.get_piece(single_rank, file) is None
                    and self.board.get_piece(double_rank, file) is None
                ):
                    moves.append(Move(rank, file, double_rank, file))

        # Captures (including en passant)
        for df in [-1, 1]:
            new_file = file + df
            if not (0 <= new_file < 8):
                continue

            new_rank = rank + direction
            if not (0 <= new_rank < 8):
                continue

            target = self.board.get_piece(new_rank, new_file)

            # Regular capture
            if target and target.color != piece.color:
                if new_rank == promotion_rank:
                    for promo_type in [
                        PieceType.QUEEN,
                        PieceType.ROOK,
                        PieceType.BISHOP,
                        PieceType.KNIGHT,
                    ]:
                        moves.append(
                            Move(
                                rank,
                                file,
                                new_rank,
                                new_file,
                                captured_piece_type=target.piece_type,
                                promotion_piece_type=promo_type,
                            )
                        )
                else:
                    moves.append(
                        Move(
                            rank,
                            file,
                            new_rank,
                            new_file,
                            captured_piece_type=target.piece_type,
                        )
                    )

            # En passant
            elif self.board.en_passant_square == (new_rank, new_file):
                moves.append(
                    Move(
                        rank,
                        file,
                        new_rank,
                        new_file,
                        captured_piece_type=PieceType.PAWN,
                        is_en_passant=True,
                    )
                )

        return moves

    def _generate_knight_moves(self, rank: int, file: int, piece) -> List[Move]:
        """Generate all knight moves from the given position."""
        moves = []
        # Knight moves: 2 squares in one direction, 1 in perpendicular
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
                target = self.board.get_piece(new_rank, new_file)
                if target is None:
                    moves.append(Move(rank, file, new_rank, new_file))
                elif target.color != piece.color:
                    moves.append(
                        Move(
                            rank,
                            file,
                            new_rank,
                            new_file,
                            captured_piece_type=target.piece_type,
                        )
                    )

        return moves

    def _generate_sliding_moves(
        self, rank: int, file: int, piece, directions: List[Tuple[int, int]]
    ) -> List[Move]:
        """
        Generate sliding piece moves (bishop, rook, queen).

        Args:
            rank: Starting rank
            file: Starting file
            piece: The piece being moved
            directions: List of (rank_delta, file_delta) tuples for movement directions
        """
        moves = []

        for dr, df in directions:
            # Slide in this direction until blocked
            new_rank = rank + dr
            new_file = file + df

            while 0 <= new_rank < 8 and 0 <= new_file < 8:
                target = self.board.get_piece(new_rank, new_file)

                if target is None:
                    # Empty square - can move here
                    moves.append(Move(rank, file, new_rank, new_file))
                elif target.color != piece.color:
                    # Enemy piece - can capture
                    moves.append(
                        Move(
                            rank,
                            file,
                            new_rank,
                            new_file,
                            captured_piece_type=target.piece_type,
                        )
                    )
                    break  # Can't move past this piece
                else:
                    # Own piece - blocked
                    break

                new_rank += dr
                new_file += df

        return moves

    def _generate_bishop_moves(self, rank: int, file: int, piece) -> List[Move]:
        """Generate all bishop moves from the given position."""
        # Diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._generate_sliding_moves(rank, file, piece, directions)

    def _generate_rook_moves(self, rank: int, file: int, piece) -> List[Move]:
        """Generate all rook moves from the given position."""
        # Horizontal and vertical directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._generate_sliding_moves(rank, file, piece, directions)

    def _generate_queen_moves(self, rank: int, file: int, piece) -> List[Move]:
        """Generate all queen moves from the given position."""
        # All eight directions (combination of rook and bishop)
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        return self._generate_sliding_moves(rank, file, piece, directions)

    def _generate_king_moves(self, rank: int, file: int, piece) -> List[Move]:
        """Generate all king moves from the given position, including castling."""
        moves = []

        # Regular king moves (one square in any direction)
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                if dr == 0 and df == 0:
                    continue

                new_rank = rank + dr
                new_file = file + df

                if 0 <= new_rank < 8 and 0 <= new_file < 8:
                    target = self.board.get_piece(new_rank, new_file)
                    if target is None:
                        moves.append(Move(rank, file, new_rank, new_file))
                    elif target.color != piece.color:
                        moves.append(
                            Move(
                                rank,
                                file,
                                new_rank,
                                new_file,
                                captured_piece_type=target.piece_type,
                            )
                        )

        # Castling
        moves.extend(self._generate_castling_moves(rank, file, piece))

        return moves

    def _generate_castling_moves(self, rank: int, file: int, piece) -> List[Move]:
        """Generate castling moves for the king."""
        moves = []
        color = piece.color

        # Can't castle if king is in check
        if self.board.is_square_attacked(rank, file, color):
            return moves

        # Check kingside castling
        if (
            self.board.castling_rights[color]["kingside"]
            and self.board.get_piece(rank, 5) is None
            and self.board.get_piece(rank, 6) is None
            and not self.board.is_square_attacked(rank, 5, color)
            and not self.board.is_square_attacked(rank, 6, color)
        ):
            moves.append(Move(rank, file, rank, 6, is_castling=True))

        # Check queenside castling
        if (
            self.board.castling_rights[color]["queenside"]
            and self.board.get_piece(rank, 1) is None
            and self.board.get_piece(rank, 2) is None
            and self.board.get_piece(rank, 3) is None
            and not self.board.is_square_attacked(rank, 3, color)
            and not self.board.is_square_attacked(rank, 2, color)
        ):
            moves.append(Move(rank, file, rank, 2, is_castling=True))

        return moves

    def _is_legal(self, move: Move) -> bool:
        """
        Check if a move is legal (doesn't leave own king in check).

        Args:
            move: The move to check

        Returns:
            True if the move is legal, False otherwise
        """
        # Make the move
        self.board.make_move(move)

        # Check if our king is in check after the move
        is_legal = not self.board.is_in_check(self.board.opponent_color())

        # Unmake the move
        self.board.unmake_move()

        return is_legal
