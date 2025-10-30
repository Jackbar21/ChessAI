"""Utility functions for testing the Chess AI Engine."""

from typing import List, Tuple
from src import Board, Move, Piece, PieceType, Color


def setup_position_from_fen(board: Board, fen: str) -> None:
    """
    Set up a board position from FEN notation (simplified version).
    Only handles piece placement, not full FEN.

    Example: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    """
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.white_pieces = set()
    board.black_pieces = set()

    piece_map = {
        "p": (PieceType.PAWN, Color.BLACK),
        "n": (PieceType.KNIGHT, Color.BLACK),
        "b": (PieceType.BISHOP, Color.BLACK),
        "r": (PieceType.ROOK, Color.BLACK),
        "q": (PieceType.QUEEN, Color.BLACK),
        "k": (PieceType.KING, Color.BLACK),
        "P": (PieceType.PAWN, Color.WHITE),
        "N": (PieceType.KNIGHT, Color.WHITE),
        "B": (PieceType.BISHOP, Color.WHITE),
        "R": (PieceType.ROOK, Color.WHITE),
        "Q": (PieceType.QUEEN, Color.WHITE),
        "K": (PieceType.KING, Color.WHITE),
    }

    ranks = fen.split("/")
    for rank_idx, rank_str in enumerate(ranks):
        rank = 7 - rank_idx  # FEN starts from rank 8
        file = 0

        for char in rank_str:
            if char.isdigit():
                file += int(char)
            elif char in piece_map:
                piece_type, color = piece_map[char]
                board.set_piece(rank, file, Piece(piece_type, color))
                file += 1


def create_position(board: Board, pieces: List[Tuple[str, str]]) -> None:
    """
    Set up a position from a list of (piece, square) tuples.
    
    Args:
        board: The board to set up
        pieces: List of (piece_notation, square) e.g. [("K", "e1"), ("k", "e8")]
    """
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.white_pieces = set()
    board.black_pieces = set()
    
    # Disable all castling rights for test positions (can be re-enabled if needed)
    board.castling_rights.white_kingside = False
    board.castling_rights.white_queenside = False
    board.castling_rights.black_kingside = False
    board.castling_rights.black_queenside = False

    piece_map = {
        "P": (PieceType.PAWN, Color.WHITE),
        "N": (PieceType.KNIGHT, Color.WHITE),
        "B": (PieceType.BISHOP, Color.WHITE),
        "R": (PieceType.ROOK, Color.WHITE),
        "Q": (PieceType.QUEEN, Color.WHITE),
        "K": (PieceType.KING, Color.WHITE),
        "p": (PieceType.PAWN, Color.BLACK),
        "n": (PieceType.KNIGHT, Color.BLACK),
        "b": (PieceType.BISHOP, Color.BLACK),
        "r": (PieceType.ROOK, Color.BLACK),
        "q": (PieceType.QUEEN, Color.BLACK),
        "k": (PieceType.KING, Color.BLACK),
    }

    for piece_char, square in pieces:
        if piece_char not in piece_map:
            raise ValueError(f"Unknown piece: {piece_char}")

        piece_type, color = piece_map[piece_char]
        rank, file = board.notation_to_square(square)
        board.set_piece(rank, file, Piece(piece_type, color))


def get_move_by_notation(board: Board, move_str: str) -> Move:
    """
    Find a move by algebraic notation (e.g., "e2e4").

    Args:
        board: The current board state
        move_str: Move in format "from_square to_square" (e.g., "e2e4")

    Returns:
        The Move object
    """
    if len(move_str) < 4:
        raise ValueError(f"Invalid move notation: {move_str}")

    from_square = move_str[:2]
    to_square = move_str[2:4]

    from_rank, from_file = board.notation_to_square(from_square)
    to_rank, to_file = board.notation_to_square(to_square)

    piece = board.get_piece(from_rank, from_file)
    if not piece:
        raise ValueError(f"No piece at {from_square}")

    # Check if it's a capture
    target = board.get_piece(to_rank, to_file)
    captured_type = target.piece_type if target else None

    # Check for promotion
    promotion = None
    if len(move_str) > 4:
        promo_char = move_str[4].lower()
        promo_map = {
            "q": PieceType.QUEEN,
            "r": PieceType.ROOK,
            "b": PieceType.BISHOP,
            "n": PieceType.KNIGHT,
        }
        promotion = promo_map.get(promo_char)

    return Move(
        from_rank,
        from_file,
        to_rank,
        to_file,
        captured_piece_type=captured_type,
        promotion_piece_type=promotion,
    )


def count_pieces(board: Board) -> dict:
    """Count all pieces on the board by type and color."""
    counts = {
        Color.WHITE: {pt: 0 for pt in PieceType},
        Color.BLACK: {pt: 0 for pt in PieceType},
    }

    for rank in range(8):
        for file in range(8):
            piece = board.get_piece(rank, file)
            if piece:
                counts[piece.color][piece.piece_type] += 1

    return counts


def print_position(board: Board, label: str = "") -> None:
    """Print a board position with optional label."""
    if label:
        print(f"\n{label}")
    print(board.display())
    print(f"Turn: {board.turn.name}")
    print(f"Evaluation: {board.evaluate()}")
