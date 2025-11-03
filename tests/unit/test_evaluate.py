from src import Board, PieceType
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
