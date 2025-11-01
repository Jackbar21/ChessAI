"""
Tests for game over conditions in the Chess AI Engine.
"""

import pytest
from src.piece import Piece
from src.board import Board
from src.move import Move
from src.constants import Color, PieceType
from src.movegen import MoveGenerator
from utils.utils import get_move


def test_not_over():
    """Game is ongoing, should not be over."""
    board = Board()
    board.setup_initial_position()
    assert not board.is_game_over()


def test_checkmate():
    """Test a checkmate position (Scholars's Mate)."""
    board = Board()
    board.setup_initial_position()
    # Scholar's mate position: 1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 4. Qxf7#
    moves = [
        get_move("e2", "e4"),  # e4
        get_move("e7", "e5"),  # e5
        get_move("d1", "h5"),  # Qh5
        get_move("b8", "c6"),  # Nc6
        get_move("f1", "c4"),  # Bc4
        get_move("g8", "f6"),  # Nf6
        get_move("h5", "f7"),  # Qxf7#
    ]
    for move in moves:
        board.make_move(move)
        print()
        print(board.display())
        print()

    assert board.is_game_over()
    assert board.is_in_check(Color.BLACK)
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    assert len(legal_moves) == 0  # No legal moves for black


def test_stalemate():
    """Set up a known stalemate position."""
    # Black king on h8, white king on f7, white queen on g6, black to move
    fen = "7k/5K2/6Q1/8/8/8/8/8 b - - 0 1"
    board = Board()
    board.from_fen(fen)
    print(board.display())
    assert board.is_game_over()


def test_threefold_repetition():
    """Test threefold repetition."""
    board = Board()
    board.setup_initial_position()

    move1 = get_move("g1", "f3")  # Nf3
    move2 = get_move("b8", "c6")  # Nc6
    move3 = get_move("f3", "g1")  # Ng1
    move4 = get_move("c6", "b8")  # Nb8

    # Repeat moves 3 times
    for _ in range(3):
        board.make_move(move1)
        board.make_move(move2)
        board.make_move(move3)
        board.make_move(move4)

    assert board.is_game_over()


def test_insufficient_material():
    """Test insufficient material: King vs King."""
    board = Board()

    fen = "7k/8/8/8/8/8/8/K7 w - - 0 1"
    board.from_fen(fen)
    print(board.display())

    assert board.is_game_over()
