from src import Board, PieceType


def is_endgame(board: Board) -> bool:
    """
    Determine if the game is in the endgame phase based on material.
    Simple heuristic: 4 or fewer major/minor pieces (non-pawn, non-king) on the board.
    """
    major_minor_count = 0

    # Count white major/minor pieces
    for _, _, piece in board.white_pieces:
        if piece.piece_type not in (PieceType.PAWN, PieceType.KING):
            major_minor_count += 1
            if major_minor_count > 4:
                return False

    # Count black major/minor pieces
    for _, _, piece in board.black_pieces:
        if piece.piece_type not in (PieceType.PAWN, PieceType.KING):
            major_minor_count += 1
            if major_minor_count > 4:
                return False

    return major_minor_count <= 4
