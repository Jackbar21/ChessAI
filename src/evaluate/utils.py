from src import Board, PieceType


def is_endgame(board: Board) -> bool:
    """
    Determine if the game is in the endgame phase based on material.
    Simple heuristic: 4 or fewer major/minor pieces (non-pawn, non-king) on the board.
    """
    major_minor_count = 0
    for rank in range(8):
        for file in range(8):
            piece = board.get_piece(rank, file)
            if piece and piece.piece_type not in (PieceType.PAWN, PieceType.KING):
                major_minor_count += 1
    return major_minor_count <= 4
