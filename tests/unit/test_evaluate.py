from src import Board, Color, Piece, PieceType, Move
from src.evaluate.evaluate import evaluate
from src.evaluate.material import evaluate as material
from src.evaluate.pst import evaluate as pst


def test_material():
    """Test the material evaluation function."""
    board = Board()
    board.setup_initial_position()

    # Initial position should be equal
    score = material(board)
    assert score == 0, f"Expected 0, got {score}"

    # Remove a black pawn
    black_pawn_rank, black_pawn_file = board.notation_to_square("e7")
    board.set_piece(black_pawn_rank, black_pawn_file, None)

    score = material(board)
    expected_score = PieceType.PAWN.centipawn_value
    assert score == expected_score, f"Expected {expected_score}, got {score}"

    # Remove a white knight
    white_knight_rank, white_knight_file = board.notation_to_square("b1")
    board.set_piece(white_knight_rank, white_knight_file, None)

    score = material(board)
    expected_score = PieceType.PAWN.centipawn_value - PieceType.KNIGHT.centipawn_value
    assert score == expected_score, f"Expected {expected_score}, got {score}"


def test_pst():
    """Test the piece-square table evaluation function."""
    board = Board()
    board.setup_initial_position()

    # Initial position should be equal
    score = pst(board)
    assert score == 0, f"Expected 0, got {score}"

    # Move pawn to d4
    move = board.get_move_from_uci("d2d4")
    board.make_move(move)

    score = pst(board)
    assert score > 0, f"Expected positive score for white pawn on d4, got {score}"

    # Move black knight to f6
    move = board.get_move_from_uci("g8f6")
    board.make_move(move)

    score = pst(board)
    assert (
        score < 0
    ), f"Expected negative score for white after black knight moved to f6, got {score}"


# region Endgame / Major-Minor Piece Count Tests
def count_actual_major_minor(board: Board) -> int:
    """Helper: counts major/minor pieces directly from board for verification."""
    count = 0
    for rank in range(8):
        for file in range(8):
            piece = board.get_piece(rank, file)
            if piece and piece.piece_type in [
                PieceType.QUEEN,
                PieceType.ROOK,
                PieceType.BISHOP,
                PieceType.KNIGHT,
            ]:
                count += 1
    return count


def test_initial_board_counts():
    board = Board()
    board.setup_initial_position()
    # 7 major/minor per side => 14 total
    assert board.major_minor_count == 14
    assert board.major_minor_count == count_actual_major_minor(board)


def test_set_piece_updates_count():
    board = Board()
    assert board.major_minor_count == 0

    # Place white & black kings (should not affect count)
    board.set_piece(0, 4, Piece(PieceType.KING, Color.WHITE))
    board.set_piece(7, 4, Piece(PieceType.KING, Color.BLACK))
    assert board.major_minor_count == 0

    # Place a white queen
    board.set_piece(0, 3, Piece(PieceType.QUEEN, Color.WHITE))
    assert board.major_minor_count == 1

    # Place a black pawn (should not affect count)
    board.set_piece(1, 0, Piece(PieceType.PAWN, Color.BLACK))
    assert board.major_minor_count == 1  # No change

    # Place a white knight
    board.set_piece(0, 1, Piece(PieceType.KNIGHT, Color.WHITE))
    assert board.major_minor_count == 2

    # Place a black bishop
    board.set_piece(7, 2, Piece(PieceType.BISHOP, Color.BLACK))
    assert board.major_minor_count == 3

    # Place a white rook
    board.set_piece(0, 0, Piece(PieceType.ROOK, Color.WHITE))
    assert board.major_minor_count == 4

    # Remove the white queen
    board.set_piece(0, 3, None)
    assert board.major_minor_count == 3

    # Remove the black pawn (should not affect count)
    board.set_piece(1, 0, None)
    assert board.major_minor_count == 3  # No change


def test_make_move_and_capture():
    board = Board()
    board.setup_initial_position()
    assert board.major_minor_count == 14

    # Move white knight (no capture)
    move = board.get_move_from_uci("g1f3")
    board.make_move(move)
    assert board.major_minor_count == 14

    # Move black knight (no capture)
    move = board.get_move_from_uci("b8c6")
    board.make_move(move)
    assert board.major_minor_count == 14

    # Move white knight into black knight's attack range (no capture)
    move = board.get_move_from_uci("f3e5")
    board.make_move(move)
    assert board.major_minor_count == 14

    # Capture: black knight captures white knight
    move = board.get_move_from_uci("c6e5")
    board.make_move(move)
    # Total decreases by 1
    assert board.major_minor_count == 13

    # Undo capture
    board.unmake_move()
    assert board.major_minor_count == 14


def test_promotion_updates_count():
    board = Board()
    # Empty board
    board.major_minor_count = 0
    # Place a white pawn ready to promote
    pawn = Piece(PieceType.PAWN, Color.WHITE)
    board.set_piece(6, 0, pawn)

    # Promotion move to queen
    move = Move(
        from_rank=6,
        from_file=0,
        to_rank=7,
        to_file=0,
        promotion_piece_type=PieceType.QUEEN,
    )
    board.make_move(move)
    # Total count increases
    assert board.major_minor_count == 1

    board.unmake_move()
    assert board.major_minor_count == 0


def test_randomized_consistency():
    """Optional: check that major_minor_count matches actual board every time."""
    import random

    board = Board()
    board.setup_initial_position()
    for _ in range(100):
        # Pick a random square
        rank = random.randint(0, 7)
        file = random.randint(0, 7)
        # Place or remove a random major/minor piece
        if random.random() < 0.5:
            piece_type = random.choice(
                [PieceType.KNIGHT, PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]
            )
            color = random.choice([Color.WHITE, Color.BLACK])
            board.set_piece(rank, file, Piece(piece_type, color))
        else:
            board.set_piece(rank, file, None)
        assert board.major_minor_count == count_actual_major_minor(board)


# endregion
