import pytest
from src import Board, MoveGenerator, RandomAgent, Color, PieceType, Move


def test_not_over():
    """Game is ongoing, should not be over."""
    board = Board()
    board.setup_initial_position()
    assert not board.is_game_over()


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
