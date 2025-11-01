"""
Regression tests to ensure that previously identified bugs do not reoccur.
"""

from src import Board, MoveGenerator


def test_random_agent_illegal_move_regression():
    """
    Recreates a historical bug where RandomAgent tried to play an illegal move (c3b4).
    This should never be legal in the given position.
    """
    moves = (
        "b2b3 e7e5 g2g4 f7f5 e2e4 g7g5 f1c4 h7h5 h2h4 d7d5 h1h3 c7c5 "
        "c4f1 b7b5 f1b5 e8e7 h3d3 a7a5 d1f3 b8c6 f3h1 c8a6 e4d5 a8b8 "
        "c2c4 d8d7 d3d4 f8g7 h1h2 g8f6 h2e5 e7f8 e5c7 g7h6 e1e2 f8g7 "
        "b5a6 f6e4 e2d1 e4c3 d1e1 c3e2 b1a3 e2g3 b3b4 g3e4 a6b7 e4f6 "
        "d2d3 f6g4 b4a5 g4h2 c7b6 h2f3 g1f3 h8e8 f3e5 e8f8 e1d1 f8e8 "
        "b6b1 e8e5 d5d6 e5e1 d1d2 e1e2 d2d1 e2e1 d1c2 e1e2 c2d1 e2d2 "
        "d1d2 c6b4 f2f3 b4c2 b1b2 c2e1 d4g4 g7h7 a3b1 h6g7 f3f4 g7c3 "
        "b1c3 d7e6 c3b5 e6e2 d2c3 e2c2"
    )

    board = Board()
    board.setup_initial_position()
    movegen = MoveGenerator(board)

    # Replay all moves up to the problematic position
    for move_str in moves.split():
        move = board.get_move_from_uci(move_str)
        legal_moves = movegen.generate_legal_moves()
        assert move in legal_moves, f"Move {move_str} should be legal"
        board.make_move(move)

    # Now check that c3b4 is *not* legal
    illegal_move = board.get_move_from_uci("c3b4")
    legal_moves = movegen.generate_legal_moves()
    assert illegal_move not in legal_moves, f"Move {illegal_move} should be illegal"


def test_minimax_agent_depth2_regression():
    """
    Regression test for a historical bug where MinimaxAgent at depth=2
    crashed when I tried kingside castling against it (e1g1 move).
    """

    # Moves to reach the problematic position
    moves = "d2d4 g7g6 c2c4 b7b6 b1c3 c8b7 e2e4 g8f6 g1f3 f6e4 c3e4 b7e4 c1f4 e4c6 f1d3 c6b7 d1e2 d8c8 e1g1 h7h6 f1e1"

    board = Board()
    board.setup_initial_position()
    movegen = MoveGenerator(board)

    # Replay all moves
    for move_str in moves.split():
        move = board.get_move_from_uci(move_str)
        legal_moves = movegen.generate_legal_moves()
        assert move in legal_moves, f"Move {move_str} should be legal"
        board.make_move(move)
