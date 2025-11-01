"""
Tests for game over conditions in the Chess AI Engine.
"""

import pytest
from src.piece import Piece
from src.board import Board
from src.move import Move
from src.constants import Color, PieceType
from src.movegen import MoveGenerator


def test_not_over():
    """Game is ongoing, should not be over."""
    board = Board()
    board.setup_initial_position()
    assert not board.is_game_over()


def test_checkmate():
    """Test a checkmate position (Scholar's Mate)."""
    board = Board()
    board.setup_initial_position()
    # Scholar's mate position: 1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 4. Qxf7#
    moves = [
        Move.from_uci("e2e4"),  # e4
        Move.from_uci("e7e5"),  # e5
        Move.from_uci("d1h5"),  # Qh5
        Move.from_uci("b8c6"),  # Nc6
        Move.from_uci("f1c4"),  # Bc4
        Move.from_uci("g8f6"),  # Nf6
        Move.from_uci("h5f7"),  # Qxf7#
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

    # Initial board position technically counts as first occurrence

    # This sequence of 4 moves will return to the initial position
    move1 = Move.from_uci("g1f3")  # Nf3
    move2 = Move.from_uci("b8c6")  # Nc6
    move3 = Move.from_uci("f3g1")  # Ng1
    move4 = Move.from_uci("c6b8")  # Nb8

    board.make_move(move1)
    board.make_move(move2)
    board.make_move(move3)
    board.make_move(move4)

    # We have now repeated the initial position twice
    assert not board.is_game_over()

    board.make_move(move1)
    board.make_move(move2)
    board.make_move(move3)

    # We still have not reached threefold repetition
    assert not board.is_game_over()
    board.make_move(move4)

    # Now we should have reached threefold repetition
    assert board.is_game_over()


def test_insufficient_material():
    """Test insufficient material: King vs King."""
    board = Board()

    fen = "7k/8/8/8/8/8/8/K7 w - - 0 1"
    board.from_fen(fen)
    print(board.display())

    assert board.is_game_over()


def test_50_move_rule():
    """Test 50-move rule."""
    board = Board()
    fen = "6kr/7p/8/8/8/8/8/KR6 w - - 99 65"
    board.from_fen(fen)

    assert not board.is_game_over()

    move = Move.from_uci("a1a2")
    board.make_move(move)

    assert board.is_game_over()
