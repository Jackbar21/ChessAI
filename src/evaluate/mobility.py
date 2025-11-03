# src/evaluate/mobility.py
from src import Board, Color, MoveGenerator

MOBILITY_WEIGHT = 5  # ~3-7 centipawns is common


def evaluate(board: Board) -> int:
    """
    Evaluate mobility (number of legal moves difference between White and Black).
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

    score = (len(white_moves) - len(black_moves)) * MOBILITY_WEIGHT
    return score
