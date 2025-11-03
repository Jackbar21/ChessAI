"""
Regression tests to ensure that previously identified bugs do not reoccur.
"""

from src import Board, MoveGenerator, MinimaxAgent
from src.evaluate.evaluate import evaluate


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
    crashed due to castling bug. Program thought rook was still on h1
    after white castled kingside. So when trying to move f1 rook to e1,
    the program crashed.
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


def test_castling_priority():
    """
    This is a game that I was playing against MinimaxAgent with depth=2 using alpha-beta & quiescence search.
    At this point of the game, the agent decided to play Ke2 instead of another move like castling. The
    PST function should reward castling more than moving the king to e2.
    """
    board = Board()
    fen = "r2qkb1r/3b1ppp/p1p1pn2/3pN1B1/3P4/2NQ4/PPP2PPP/R3K2R w KQkq - 0 11"
    board.from_fen(fen)

    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()

    castling_move = board.get_move_from_uci("e1g1")
    king_e2_move = board.get_move_from_uci("e1e2")

    assert castling_move in legal_moves, "Castling move should be legal"
    assert king_e2_move in legal_moves, "King to e2 move should be legal"

    cur_eval = evaluate(board)

    # Make the castling move and evaluate
    board.make_move(castling_move)
    eval_after_castling = evaluate(board)
    board.unmake_move()

    # Make the king to e2 move and evaluate
    board.make_move(king_e2_move)
    eval_after_king_e2 = evaluate(board)
    board.unmake_move()

    assert eval_after_castling > cur_eval, "Castling should improve evaluation"
    assert (
        eval_after_castling > eval_after_king_e2
    ), "Castling should yield a better evaluation than king to e2"


def test_avoid_threefold_repitition_in_winning_position():
    """
    Regression test for a historical bug where the engine would
    choose moves that lead to threefold repetition even in winning positions.
    This test sets up a position where the engine is winning and ensures
    it does not choose a move that leads to repetition.
    """
    moves = "d2d4 g8f6 c1f4 b8c6 e2e3 d7d5 g1f3 c8f5 f1b5 a7a6 b5a4 e7e6 c2c3 f8d6 f4g3 d6g3 h2g3 b7b5 a4c2 f5c2 d1c2 f6e4 b1d2 e4d2 c2d2 d8d6 d2d3 h7h6 e3e4 e8g8 e4e5 d6e7 e1c1 g8h8 f3h4 e7g5 f2f4 g5g4 d1f1 b5b4 f4f5 g4g5 c1b1 b4c3 b2c3 a8b8 b1c2 a6a5 f5e6 f7e6 f1f8 b8f8 h1f1 f8f1 d3f1 g5g3 f1f8 h8h7 h4f3 g3g2 f3d2 g2g6 c2d1 g6d3 f8f3 d3f3 d2f3 h7g6 d1e2 g6f5 e2e3 a5a4 f3d2 h6h5 c3c4 d5c4 d2c4 h5h4 c4d2 h4h3 d2f3 a4a3 f3h2 c6b4 h2f1 b4a2 f1d2 h3h2 d2e4 h2h1q e4g3 f5g4 g3h1 a2c3 h1f2 g4f5 f2d3 a3a2 d3c1 a2a1q c1b3 a1e1 e3d3 c3e4 b3c5 e1c3 d3e2 e4c5 d4c5 f5e5 c5c6 g7g5 e2f2 g5g4 f2g2 c3f3 g2g1 e5d4 g1h2 e6e5 h2g1 d4d3 g1h2 d3d4 h2g1 d4d3 g1h2"
    board = Board()
    board.setup_initial_position()

    rb = Board()
    rb.from_fen("8/2p5/2P5/4p3/3k2p1/5q2/7K/8 w - - 0 1")

    for move_str in moves.split():
        move = board.get_move_from_uci(move_str)
        board.make_move(move)

    # Setup agent that was used in the game
    agent = MinimaxAgent(board)
    depth = 2

    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()

    assert (
        max(board.fen_history.values(), default=0) < 3
    ), "Position should not already be in repetition"

    repetition_move = board.get_move_from_uci("d3d4")  # Move leading to repetition
    assert repetition_move in legal_moves, "Repetition-inducing move should be legal"

    # Make repetition move, ensure it leads to threefold repetition
    board.make_move(repetition_move)
    assert (
        board.fen_history[board.position_fen()] >= 3
    ), "Making the repetition move should lead to threefold repetition"
    assert board.is_game_over(), "Game should be over due to threefold repetition"
    assert evaluate(board) == 0, "Game should be a draw due to threefold repetition"
    board.unmake_move()

    # Now let the engine choose a move (should not be the repetition move, since it's winning)
    best_move = agent.find_best_move(depth)
    assert best_move in legal_moves, "Best move should be legal"
    assert (
        best_move != repetition_move
    ), "Engine should avoid moves leading to threefold repetition in winning positions"
    board.make_move(best_move)
    assert (
        board.fen_history[board.position_fen()] < 3
    ), "Engine's move should not lead to threefold repetition"
    assert not board.is_game_over(), "Game should not be over after engine's move"
    assert (
        evaluate(board) < 0
    ), "Engine (playing black) should maintain winning position after its move"
