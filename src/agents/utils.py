from src import Board, Move


def evaluate_move(move: Move) -> int:
    """
    Move evaluation for move ordering.
    Purpose: Alpha-Beta pruning is more effective when better moves are searched first,
    as it increases the chances of pruning branches early.
    """
    score = 0

    # Prioritize captures
    if move.captured_piece_type is not None:
        score += move.captured_piece_type.centipawn_value * 10

    # Prioritize promotions
    if move.promotion_piece_type is not None:
        score += move.promotion_piece_type.centipawn_value * 20

    # Prioritize castling
    if move.is_castling:
        score += 5

    return score
