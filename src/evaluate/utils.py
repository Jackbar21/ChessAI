from src import Board


def is_endgame(board: Board) -> bool:
    """
    Determine if the game is in the endgame phase based on material.
    Simple heuristic: 4 or fewer major/minor pieces (non-pawn, non-king) on the board.
    """
    return board.major_minor_count <= 4
