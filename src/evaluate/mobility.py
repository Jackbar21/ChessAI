# src/evaluate/mobility.py
from src import Board, Color, MoveGenerator


def evaluate(board: Board) -> int:
    """
    Evaluate mobility (number of legal moves difference between White and Black).

    Returns:
        Positive if White has more mobility, negative if Black does.
    """
    movegen = MoveGenerator(board)
    moves = movegen.generate_legal_moves()

    white_moves, black_moves = [], []
    for move in moves:
        piece = board.get_piece(move.from_rank, move.from_file)
        if piece.color == Color.WHITE:
            white_moves.append(move)
        else:
            black_moves.append(move)

    weight = 5  # ~3-7 centipawns is typical weight per move
    score = (len(white_moves) - len(black_moves)) * weight
    return score
