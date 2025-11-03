from collections import defaultdict
from src import Board, Color, PieceType

# Pawn structure weights
ISOLATED_PAWN_PENALTY = 20
DOUBLED_PAWN_PENALTY = 15
PASSED_PAWN_BONUS = [0, 5, 10, 20, 35, 60, 100, 200]


def evaluate(board: Board) -> int:
    """
    Evaluate pawn structure on the board.
    TODO: Implement more features like backward pawns, pawn islands, etc.
    """
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

    score += _evaluate_pawns(white_pawns, black_pawns, Color.WHITE)
    score -= _evaluate_pawns(black_pawns, white_pawns, Color.BLACK)

    return score


def _evaluate_pawns(pawns, opponent_pawns, color: Color) -> int:
    """Return pawn structure score for given color"""
    score = 0

    files_count = defaultdict(int)
    for _, file in pawns:
        files_count[file] += 1

    for rank, file in pawns:
        # Isolated pawn
        if files_count[file - 1] == 0 and files_count[file + 1] == 0:
            score += ISOLATED_PAWN_PENALTY

        # Doubled pawn (penalty per pawn above the first on that file)
        pawn_count = files_count[file]
        if pawn_count > 1:
            score += DOUBLED_PAWN_PENALTY * (pawn_count - 1)

        # Passed pawn
        if _is_passed((rank, file), opponent_pawns, color):
            # Rank-dependent bonus
            index = rank if color == Color.WHITE else 7 - rank
            score += PASSED_PAWN_BONUS[index]

    return score


def _is_passed(pawn, opponent_pawns, color: Color) -> bool:
    """Check if pawn is a passed pawn"""
    rank, file = pawn
    for other_rank, other_file in opponent_pawns:
        if abs(other_file - file) <= 1:
            if color == Color.WHITE and other_rank > rank:
                return False
            if color == Color.BLACK and other_rank < rank:
                return False
    return True
