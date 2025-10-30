"""Tests for basic move generation and validation."""

import pytest
from src import Board, MoveGenerator, Color, PieceType
from tests.test_utils import create_position, count_pieces


def test_initial_position_move_count():
    """Test that starting position has exactly 20 legal moves."""
    board = Board()
    board.setup_initial_position()
    movegen = MoveGenerator(board)
    
    legal_moves = movegen.generate_legal_moves()
    assert len(legal_moves) == 20, "Starting position should have 20 legal moves"


def test_pawn_single_push():
    """Test pawn single push moves."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("P", "e2"), ("P", "d2"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Find pawn moves
    pawn_moves = [m for m in legal_moves if m.from_rank == 1 and m.from_file == 4]
    assert any(m.to_rank == 2 and m.to_file == 4 for m in pawn_moves), "e2-e3 should be legal"


def test_pawn_double_push():
    """Test pawn double push from starting position."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("P", "e2"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    pawn_moves = [m for m in legal_moves if m.from_rank == 1 and m.from_file == 4]
    assert any(m.to_rank == 3 and m.to_file == 4 for m in pawn_moves), "e2-e4 should be legal"


def test_pawn_capture():
    """Test pawn captures."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("P", "e4"), ("p", "d5"), ("p", "f5"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    pawn_moves = [m for m in legal_moves if m.from_rank == 3 and m.from_file == 4]
    
    # Should be able to capture on d5 and f5
    assert any(m.to_rank == 4 and m.to_file == 3 and m.captured_piece_type == PieceType.PAWN 
               for m in pawn_moves), "e4xd5 should be legal"
    assert any(m.to_rank == 4 and m.to_file == 5 and m.captured_piece_type == PieceType.PAWN 
               for m in pawn_moves), "e4xf5 should be legal"


def test_knight_moves():
    """Test knight move pattern."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("N", "d4"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    knight_moves = [m for m in legal_moves if m.from_rank == 3 and m.from_file == 3]
    
    # Knight on d4 should have 8 possible moves
    expected_squares = [
        (5, 2), (5, 4),  # c6, e6
        (4, 1), (4, 5),  # b5, f5
        (2, 1), (2, 5),  # b3, f3
        (1, 2), (1, 4),  # c2, e2
    ]
    
    assert len(knight_moves) == 8, f"Knight on d4 should have 8 moves, got {len(knight_moves)}"
    
    for rank, file in expected_squares:
        assert any(m.to_rank == rank and m.to_file == file for m in knight_moves), \
            f"Knight should be able to move to {board.square_to_notation(rank, file)}"


def test_bishop_moves():
    """Test bishop diagonal movement."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("B", "d4"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    bishop_moves = [m for m in legal_moves if m.from_rank == 3 and m.from_file == 3]
    
    # Bishop on d4 should be able to reach these squares on the diagonals
    assert len(bishop_moves) == 13, f"Bishop on d4 should have 13 moves, got {len(bishop_moves)}"


def test_rook_moves():
    """Test rook orthogonal movement."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("R", "d4"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    rook_moves = [m for m in legal_moves if m.from_rank == 3 and m.from_file == 3]
    
    # Rook on d4 should have 14 moves (7 ranks + 7 files)
    assert len(rook_moves) == 14, f"Rook on d4 should have 14 moves, got {len(rook_moves)}"


def test_queen_moves():
    """Test queen can move like rook and bishop combined."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("Q", "d4"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    queen_moves = [m for m in legal_moves if m.from_rank == 3 and m.from_file == 3]
    
    # Queen on d4 should have 27 moves (14 like rook + 13 like bishop)
    assert len(queen_moves) == 27, f"Queen on d4 should have 27 moves, got {len(queen_moves)}"


def test_king_moves():
    """Test king one-square movement."""
    board = Board()
    create_position(board, [
        ("K", "e4"), ("k", "e8"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    king_moves = [m for m in legal_moves if m.from_rank == 3 and m.from_file == 4]
    
    # King on e4 should have 8 moves
    assert len(king_moves) == 8, f"King on e4 should have 8 moves, got {len(king_moves)}"


def test_blocked_pieces():
    """Test that pieces are blocked by other pieces."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("R", "d4"), ("P", "d5"),  # Rook blocked by own pawn
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    rook_moves = [m for m in legal_moves if m.from_rank == 3 and m.from_file == 3]
    
    # Rook can't move through own pawn
    assert not any(m.to_rank >= 4 and m.to_file == 3 for m in rook_moves), \
        "Rook should be blocked by own pawn"


def test_capture_enemy_pieces():
    """Test that pieces can capture enemy pieces."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("R", "d4"), ("p", "d7"),  # Rook can capture enemy pawn
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    rook_moves = [m for m in legal_moves if m.from_rank == 3 and m.from_file == 3]
    
    # Rook can capture on d7
    assert any(m.to_rank == 6 and m.to_file == 3 and m.captured_piece_type == PieceType.PAWN 
               for m in rook_moves), "Rook should be able to capture enemy pawn"
    
    # But can't move past it
    assert not any(m.to_rank == 7 and m.to_file == 3 for m in rook_moves), \
        "Rook should not be able to move past enemy piece"


def test_pinned_piece_cannot_move():
    """Test that pinned pieces cannot move (would expose king to check)."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("N", "e2"), ("r", "e8"),  # Knight pinned by rook
        ("k", "a8"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Knight on e2 is pinned and cannot move
    knight_moves = [m for m in legal_moves if m.from_rank == 1 and m.from_file == 4]
    assert len(knight_moves) == 0, "Pinned knight should not have any legal moves"


def test_must_block_check():
    """Test that when in check, only blocking/capturing/moving king is legal."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "a1"), ("r", "e8"),  # White king in check from black rook
        ("k", "a8"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Only king moves and blocks are legal
    assert all(m.from_rank == 0 and m.from_file == 4 for m in legal_moves if m.from_rank == 0), \
        "Only king should be able to move when in check (or blocking pieces)"
