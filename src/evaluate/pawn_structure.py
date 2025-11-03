from collections import defaultdict
from src import Board, Color, PieceType

ISOLATED_PAWN_PENALTY = 20
DOUBLED_PAWN_PENALTY = 15  # Will get counted twice, e.g. 30 per pair of doubled pawns
PASSED_PAWN_BONUS = [0, 5, 10, 20, 35, 60, 100, 0]


def evaluate(board: Board) -> int:
    score = 0
    white_pawns, black_pawns = [], []

    for rank in range(8):
        for file in range(8):
            piece = board.get_piece(rank, file)
            if not piece or piece.piece_type != PieceType.PAWN:
                continue
            if piece.color == Color.WHITE:
                white_pawns.append((rank, file))
            else:
                black_pawns.append((rank, file))

    # Count pawns per file
    white_files, black_files = defaultdict(int), defaultdict(int)
    for _, file in white_pawns:
        white_files[file] += 1
    for _, file in black_pawns:
        black_files[file] += 1

    # --- White ---
    for rank, file in white_pawns:
        # Isolated pawn
        if white_files[file - 1] == 0 and white_files[file + 1] == 0:
            score -= ISOLATED_PAWN_PENALTY

        # Doubled pawn
        if white_files[file] > 1:
            score -= DOUBLED_PAWN_PENALTY

        # Passed pawn
        if is_passed((rank, file), black_pawns, Color.WHITE):
            score += PASSED_PAWN_BONUS[rank]

    # --- Black ---
    for rank, file in black_pawns:
        # Isolated pawn
        if black_files[file - 1] == 0 and black_files[file + 1] == 0:
            score += ISOLATED_PAWN_PENALTY

        # Doubled pawn
        if black_files[file] > 1:
            score += DOUBLED_PAWN_PENALTY

        # Passed pawn
        if is_passed((rank, file), white_pawns, Color.BLACK):
            score -= PASSED_PAWN_BONUS[7 - rank]

    return score


def is_passed(pawn, opponent_pawns, color):
    rank, file = pawn
    for other_rank, other_file in opponent_pawns:
        if abs(other_file - file) <= 1:
            if color == Color.WHITE and other_rank > rank:
                return False
            if color == Color.BLACK and other_rank < rank:
                return False
    return True
