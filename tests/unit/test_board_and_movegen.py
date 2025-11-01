import pytest
from src import Board, MoveGenerator, Color, PieceType
from random import choice as random_choice


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

    assert board.get_move_from_uci("e2e4") in legal_moves, "Move e2-e4 should be legal"
    assert (
        board.get_move_from_uci("e2e5") not in legal_moves
    ), "Move e2-e5 should not be legal"

    assert board.get_move_from_uci("b1c3") in legal_moves, "Move Nb1-c3 should be legal"
    assert (
        board.get_move_from_uci("b1d2") not in legal_moves
    ), "Move Nb1-d2 should not be legal"


def test_make_unmake_move():
    """Test making and unmaking moves."""
    board = Board()
    board.setup_initial_position()

    move = board.get_move_from_uci("e2e4")
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
    print(board)

    # After unmake, e2 should have the pawn again and e4 should be empty
    board.unmake_move()
    piece = board.get_piece(e2_rank, e2_file)
    assert piece is not None
    assert piece.piece_type == PieceType.PAWN
    assert piece.color == Color.WHITE
    assert board.get_piece(e4_rank, e4_file) is None
    print("\nAfter unmaking move e2-e4:\n")
    print(board)


def test_check_detection():
    """Test check detection."""
    board = Board()
    board.setup_initial_position()

    # Create a position with check
    uci_moves = [
        "b1c3",  # Nc3
        "e7e5",  # e5
        "c3d5",  # Nd5
        "d8h4",  # Qh4
        "d5c7",  # Nc7+
    ]

    checks = []
    for i, move in enumerate(uci_moves):
        move = board.get_move_from_uci(move)
        board.make_move(move)
        in_check = board.is_in_check(board.turn)
        checks.append(in_check)

    # Assert every move except the last does not put black in check
    for i in range(len(uci_moves) - 1):
        assert not checks[i], f"Move {i+1} should not put black in check"
    assert checks[-1], "Last move should put black in check"

    # Black has no legal moves, should be checkmate
    assert board.is_in_check(Color.BLACK), "Black should be in check"


def test_checkmate():
    """Test a checkmate position (Scholar's Mate)."""
    board = Board()
    board.setup_initial_position()
    # Scholar's mate position: 1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 4. Qxf7#
    uci_moves = [
        "e2e4",  # e4
        "e7e5",  # e5
        "d1h5",  # Qh5
        "b8c6",  # Nc6
        "f1c4",  # Bc4
        "g8f6",  # Nf6
        "h5f7",  # Qxf7#
    ]
    for move in uci_moves:
        move = board.get_move_from_uci(move)
        board.make_move(move)

    # Black has no legal moves, should be checkmate
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    assert len(legal_moves) == 0, "Black should have no legal moves (checkmate)"
    assert board.is_in_check(Color.BLACK), "Black should be in check"
    assert board.is_game_over(), "Game should be over (checkmate)"


def test_stalemate():
    """Set up a known stalemate position."""
    # Black king on h8, white king on f7, white queen on g6, black to move
    fen = "7k/5K2/6Q1/8/8/8/8/8 b - - 0 1"
    board = Board()
    board.from_fen(fen)
    print(board)
    assert board.is_game_over()


def test_threefold_repetition():
    """Test threefold repetition."""
    board = Board()
    board.setup_initial_position()

    # Initial board position technically counts as first occurrence

    # This sequence of 4 moves will return to the initial position
    uci_move1 = "g1f3"  # Nf3
    uci_move2 = "b8c6"  # Nc6
    uci_move3 = "f3g1"  # Ng1
    uci_move4 = "c6b8"  # Nb8

    board.make_move(board.get_move_from_uci(uci_move1))
    board.make_move(board.get_move_from_uci(uci_move2))
    board.make_move(board.get_move_from_uci(uci_move3))
    board.make_move(board.get_move_from_uci(uci_move4))

    # We have now repeated the initial position twice
    assert not board.is_game_over()

    board.make_move(board.get_move_from_uci(uci_move1))
    board.make_move(board.get_move_from_uci(uci_move2))
    board.make_move(board.get_move_from_uci(uci_move3))

    # We still have not reached threefold repetition
    assert not board.is_game_over()
    board.make_move(board.get_move_from_uci(uci_move4))

    # Now we should have reached threefold repetition
    assert board.is_game_over()


def test_insufficient_material():
    """Test insufficient material: King vs King."""
    board = Board()

    fen = "7k/8/8/8/8/8/8/K7 w - - 0 1"
    board.from_fen(fen)
    print(board)

    assert board.is_game_over()


def test_50_move_rule():
    """Test 50-move rule."""
    board = Board()
    fen = "6kr/7p/8/8/8/8/8/KR6 w - - 99 65"
    board.from_fen(fen)

    assert not board.is_game_over()

    move = board.get_move_from_uci("a1a2")
    board.make_move(move)

    assert board.is_game_over()


def test_castling_available():
    board = Board()
    fen = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"  # All four castling rights available
    board.from_fen(fen)

    white_kingside_castle = board.get_move_from_uci("e1g1")
    white_queenside_castle = board.get_move_from_uci("e1c1")
    black_kingside_castle = board.get_move_from_uci("e8g8")
    black_queenside_castle = board.get_move_from_uci("e8c8")
    print(board)

    # Assert white can castle both sides, then choose one
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    print(f"Legal moves: {[move.to_uci() for move in legal_moves]}")
    assert (
        white_kingside_castle in legal_moves
    ), "White kingside castling should be legal"
    assert (
        white_queenside_castle in legal_moves
    ), "White queenside castling should be legal"
    board.make_move(random_choice([white_kingside_castle, white_queenside_castle]))
    print(board)

    # Now black to move, assert black can castle both sides, then choose one
    legal_moves = movegen.generate_legal_moves()
    assert (
        black_kingside_castle in legal_moves
    ), "Black kingside castling should be legal"
    assert (
        black_queenside_castle in legal_moves
    ), "Black queenside castling should be legal"
    board.make_move(random_choice([black_kingside_castle, black_queenside_castle]))
    print(board)


def test_castling_not_available():
    board = Board()
    fen = "r3k2r/8/8/8/8/8/8/R3K2R w - - 0 1"  # All four castling rights not available
    board.from_fen(fen)

    white_kingside_castle = board.get_move_from_uci("e1g1")
    white_queenside_castle = board.get_move_from_uci("e1c1")
    black_kingside_castle = board.get_move_from_uci("e8g8")
    black_queenside_castle = board.get_move_from_uci("e8c8")
    print(board)

    # Assert white cannot castle either side, then make a move
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    print(f"Legal moves: {[move.to_uci() for move in legal_moves]}")
    assert (
        white_kingside_castle not in legal_moves
    ), "White kingside castling should not be legal"
    assert (
        white_queenside_castle not in legal_moves
    ), "White queenside castling should not be legal"
    board.make_move(random_choice(legal_moves))
    print(board)

    # Now black to move, assert black cannot castle either sides, then make a move
    legal_moves = movegen.generate_legal_moves()
    assert (
        black_kingside_castle not in legal_moves
    ), "Black kingside castling should not be legal"
    assert (
        black_queenside_castle not in legal_moves
    ), "Black queenside castling should not be legal"
    board.make_move(random_choice(legal_moves))
    print(board)


@pytest.mark.parametrize(
    "fen,can_castle",
    [
        ("4k3/8/8/8/8/8/8/4K2R w K - 0 1", True),  # can castle
        ("4k3/8/8/b7/8/8/8/4K2R w K - 0 1", False),  # cannot castle while in check
        ("4k3/8/8/1b6/8/8/8/4K2R w K - 0 1", False),  # cannot castle over check
        ("4k3/8/8/2b5/8/8/8/4K2R w K - 0 1", False),  # cannot castle into check
        ("4k3/8/8/3b4/8/8/8/4K2R w K - 0 1", True),  # can castle
    ],
)
def test_castling_rules(fen: str, can_castle: bool):
    """Test cannot caste in check, over check, or into check."""
    board = Board()
    board.from_fen(fen)

    white_kingside_castle = board.get_move_from_uci("e1g1")
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()

    expected = can_castle
    actual = white_kingside_castle in legal_moves
    assert (
        expected == actual
    ), f"Expected can castle: {expected}, but got {actual} for position:\n{board}"
