from src import Board, Color


def material(board: Board) -> int:
    """
    Simple material evaluation.

    Returns:
        Evaluation score in centipawns
    """
    score = 0
    for rank in range(8):
        for file in range(8):
            piece = board.get_piece(rank, file)
            if piece:
                value = piece.piece_type.centipawn_value
                if piece.color == Color.WHITE:
                    score += value
                else:
                    score -= value
    return score
