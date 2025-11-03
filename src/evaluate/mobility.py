# src/evaluate/mobility.py
from src import Board, Color, MoveGenerator, PieceType
from .utils import is_endgame

# ~3-7 centipawns is common
# NOTE: I'm using an extremely low weight of 0.1, to prioritize material
# piece-square tables more. Otherwise, to overlook good moves such
# as castling to prioritize mobility too much.
MOBILITY_WEIGHT = 0.1


def evaluate(board: Board) -> float:
    """
    Evaluate mobility (number of legal moves difference between White and Black).
    TODO: Invest in optimizations to avoid generating all moves each evaluation.
    This can include caching legal moves into the Board class, including legal-move
    restoration after making/unmaking moves.
    """
    # Generate all pseudo-legal moves instead of legal moves for efficiency
    movegen = MoveGenerator(board)

    white_moves = movegen.generate_pseudo_legal_moves_for_color(Color.WHITE)
    black_moves = movegen.generate_pseudo_legal_moves_for_color(Color.BLACK)

    white_move_count = len(white_moves)
    black_move_count = len(black_moves)

    # In early/midgame, king safety is more important than king mobility
    # Hence, do not count king moves unless in endgame
    if not is_endgame(board):
        # Discard white king moves
        for move in white_moves:
            piece = board.get_piece(move.from_rank, move.from_file)
            if piece and piece.piece_type == PieceType.KING:
                white_move_count -= 1

        # Discard black king moves
        for move in black_moves:
            piece = board.get_piece(move.from_rank, move.from_file)
            if piece and piece.piece_type == PieceType.KING:
                black_move_count -= 1

    score = (white_move_count - black_move_count) * MOBILITY_WEIGHT
    return score
