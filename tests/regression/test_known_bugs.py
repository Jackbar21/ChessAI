"""
As bug regression tests, ensure that previously identified bugs do not reoccur.
"""

import pytest
from src import Board, MoveGenerator, RandomAgent, Color, PieceType, Move


def test_illegal_move():
    # Board position as result from playing against RandomAgent
    # on lichess. Agent tried to play illegal move c3b4.
    # This test recreates this position, to fail until the bug is fixed.
    moves = "b2b3 e7e5 g2g4 f7f5 e2e4 g7g5 f1c4 h7h5 h2h4 d7d5 h1h3 c7c5 c4f1 b7b5 f1b5 e8e7 h3d3 a7a5 d1f3 b8c6 f3h1 c8a6 e4d5 a8b8 c2c4 d8d7 d3d4 f8g7 h1h2 g8f6 h2e5 e7f8 e5c7 g7h6 e1e2 f8g7 b5a6 f6e4 e2d1 e4c3 d1e1 c3e2 b1a3 e2g3 b3b4 g3e4 a6b7 e4f6 d2d3 f6g4 b4a5 g4h2 c7b6 h2f3 g1f3 h8e8 f3e5 e8f8 e1d1 f8e8 b6b1 e8e5 d5d6 e5e1 d1d2 e1e2 d2d1 e2e1 d1c2 e1e2 c2d1 e2d2 d1d2 c6b4 f2f3 b4c2 b1b2 c2e1 d4g4 g7h7 a3b1 h6g7 f3f4 g7c3 b1c3 d7e6 c3b5 e6e2 d2c3 e2c2"
    board = Board()
    board.setup_initial_position()
    movegen = MoveGenerator(board)

    for move_str in moves.split():
        move = Move.from_uci(move_str)
        legal_moves = movegen.generate_legal_moves()
        assert move in legal_moves, f"Move {move_str} should be legal"
        board.make_move(move)

    move = Move.from_uci("c3b4")
    legal_moves = movegen.generate_legal_moves()
    assert move not in legal_moves, f"Move {move} should be illegal"
