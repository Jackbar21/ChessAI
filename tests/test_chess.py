"""
Comprehensive test file for the Chess AI Engine.

Tests move generation, move execution, and AI search.
"""

import pytest
from src import Board, MoveGenerator, RandomAgent, Color, PieceType, Move


def test_move_generation():
    """Test basic move generation."""
    board = Board()
    board.setup_initial_position()
    movegen = MoveGenerator(board)

    legal_moves = movegen.generate_legal_moves()
    print(f"Legal moves from starting position: {len(legal_moves)}")
    assert len(legal_moves) == 20, "Expected 20 legal moves in starting position"

    assert Move.from_uci("e2e4") in legal_moves, "Move e2-e4 should be legal"
    assert Move.from_uci("e2e5") not in legal_moves, "Move e2-e5 should not be legal"

    assert Move.from_uci("b1c3") in legal_moves, "Move Nb1-c3 should be legal"
    assert Move.from_uci("b1d2") not in legal_moves, "Move Nb1-d2 should not be legal"


def test_make_unmake_move():
    """Test making and unmaking moves."""
    board = Board()
    board.setup_initial_position()

    move = Move.from_uci("e2e4")
    board.make_move(move)

    e2_rank, e2_file = board.notation_to_square("e2")
    e4_rank, e4_file = board.notation_to_square("e4")

    # The piece should now be on e4 and e2 should be empty
    piece = board.get_piece(e4_rank, e4_file)
    assert piece is not None
    assert piece.piece_type == PieceType.PAWN
    assert piece.color == Color.WHITE
    assert board.get_piece(e2_rank, e2_file) is None
    print("\nAfter making move e2-e4:\n")
    print(board.display())

    # After unmake, e2 should have the pawn again and e4 should be empty
    board.unmake_move()
    piece = board.get_piece(e2_rank, e2_file)
    assert piece is not None
    assert piece.piece_type == PieceType.PAWN
    assert piece.color == Color.WHITE
    assert board.get_piece(e4_rank, e4_file) is None
    print("\nAfter unmaking move e2-e4:\n")
    print(board.display())


def test_check_detection():
    """Test check detection."""
    board = Board()
    board.setup_initial_position()

    # Create a position with check (Scholar's Mate setup)
    moves = [
        Move.from_uci("e2e4"),  # e4
        Move.from_uci("e7e5"),  # e5
        Move.from_uci("d1h5"),  # Qh5
        Move.from_uci("b8c6"),  # Nc6
        Move.from_uci("f1c4"),  # Bc4
        Move.from_uci("g8f6"),  # Nf6
        Move.from_uci("h5f7"),  # Qxf7#
    ]

    checks = []
    for i, move in enumerate(moves):
        board.make_move(move)
        in_check = board.is_in_check(board.turn)
        checks.append(in_check)

    # Assert every move except the last does not put black in check
    for i in range(len(moves) - 1):
        assert not checks[i], f"Move {i+1} should not put black in check"
    assert checks[-1], "Last move should put black in check"

    # Black has no legal moves, should be checkmate
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    assert len(legal_moves) == 0, "Black should have no legal moves (checkmate)"
    assert board.is_in_check(Color.BLACK), "Black should be in check"


def test_random_agent_move():
    """
    Test RandomAgent's ability to select a legal move.
    Continues making random moves until checkmate/stalemate.
    """
    board = Board()
    board.setup_initial_position()
    movegen = MoveGenerator(board)
    agent = RandomAgent(board)

    move_count = 0
    while not board.is_game_over():
        move = agent.find_best_move(depth=1)

        board.make_move(move)
        move_count += 1

    print(f"Game over after {move_count} moves.")
    print(board.display())
    assert board.is_game_over(), "The game should be over"
