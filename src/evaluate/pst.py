from src import Board, Color, PieceType
from utils import is_endgame

# Pawns
PAWN_TABLE_WHITE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
PAWN_TABLE_BLACK = PAWN_TABLE_WHITE[::-1]

# Knights
KNIGHT_TABLE_WHITE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50],
]
KNIGHT_TABLE_BLACK = KNIGHT_TABLE_WHITE[::-1]

# Bishops
BISHOP_TABLE_WHITE = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20],
]
BISHOP_TABLE_BLACK = BISHOP_TABLE_WHITE[::-1]

# Rooks
ROOK_TABLE_WHITE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0],
]
ROOK_TABLE_BLACK = ROOK_TABLE_WHITE[::-1]

# Queens
QUEEN_TABLE_WHITE = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20],
]
QUEEN_TABLE_BLACK = QUEEN_TABLE_WHITE[::-1]

# Kings (Early and Middle game)
KING_TABLE_WHITE = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20],
]
KING_TABLE_BLACK = KING_TABLE_WHITE[::-1]

# Kings (Endgame)
KING_ENDGAME_TABLE_WHITE = [
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -40, -30, -20, -20, -30, -40, -50],
]
KING_ENDGAME_TABLE_BLACK = KING_ENDGAME_TABLE_WHITE[::-1]

# Piece-Square Table Mappings for non king pieces
WHITE_PST_TABLES = {
    PieceType.PAWN: PAWN_TABLE_WHITE,
    PieceType.KNIGHT: KNIGHT_TABLE_WHITE,
    PieceType.BISHOP: BISHOP_TABLE_WHITE,
    PieceType.ROOK: ROOK_TABLE_WHITE,
    PieceType.QUEEN: QUEEN_TABLE_WHITE,
}
BLACK_PST_TABLES = {
    PieceType.PAWN: PAWN_TABLE_BLACK,
    PieceType.KNIGHT: KNIGHT_TABLE_BLACK,
    PieceType.BISHOP: BISHOP_TABLE_BLACK,
    PieceType.ROOK: ROOK_TABLE_BLACK,
    PieceType.QUEEN: QUEEN_TABLE_BLACK,
}


def evaluate(board: Board) -> float:
    """
    Piece-Square Table (PST) evaluation.
    This technique assigns values to pieces based on their positions on the board.
    """
    endgame = is_endgame(board)

    score = 0.0
    for rank in range(8):
        for file in range(8):
            piece = board.get_piece(rank, file)
            if not piece:
                continue

            if piece.color == Color.WHITE:
                score += handle_white_piece(piece.piece_type, rank, file, endgame)
            else:
                score -= handle_black_piece(piece.piece_type, rank, file, endgame)

    return score


def handle_white_piece(piece_type, rank, file, is_endgame=False) -> int:
    """
    Get the PST value for a white piece based on its type and position.
    """
    if piece_type == PieceType.KING:
        return (
            KING_ENDGAME_TABLE_WHITE[rank][file]
            if is_endgame
            else KING_TABLE_WHITE[rank][file]
        )

    return WHITE_PST_TABLES[piece_type][rank][file]


def handle_black_piece(piece_type, rank, file, is_endgame=False) -> int:
    """
    Get the PST value for a black piece based on its type and position.
    """
    if piece_type == PieceType.KING:
        return (
            KING_ENDGAME_TABLE_BLACK[rank][file]
            if is_endgame
            else KING_TABLE_BLACK[rank][file]
        )

    return BLACK_PST_TABLES[piece_type][rank][file]
