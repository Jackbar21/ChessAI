"""Tests for special chess moves: castling, en passant, and promotion."""

import pytest
from src import Board, MoveGenerator, Color, PieceType, Move
from tests.test_utils import create_position


def test_kingside_castling_legal():
    """Test kingside castling when legal."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "h1"),  # White king and rook
        ("k", "e8"), ("r", "h8"),  # Black king and rook
    ])
    board.turn = Color.WHITE
    board.castling_rights[Color.WHITE]["kingside"] = True
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Should be able to castle kingside
    castling_moves = [m for m in legal_moves if m.is_castling and m.to_file == 6]
    assert len(castling_moves) == 1, "Should be able to castle kingside"


def test_queenside_castling_legal():
    """Test queenside castling when legal."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "a1"),  # White king and rook
        ("k", "e8"), ("r", "a8"),  # Black king and rook
    ])
    board.turn = Color.WHITE
    board.castling_rights[Color.WHITE]["queenside"] = True
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Should be able to castle queenside
    castling_moves = [m for m in legal_moves if m.is_castling and m.to_file == 2]
    assert len(castling_moves) == 1, "Should be able to castle queenside"


def test_castling_blocked_by_piece():
    """Test that castling is blocked by pieces between king and rook."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "h1"), ("N", "g1"),  # Knight blocks castling
        ("k", "e8"),
    ])
    board.turn = Color.WHITE
    board.castling_rights[Color.WHITE]["kingside"] = True
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Should NOT be able to castle (blocked by knight)
    castling_moves = [m for m in legal_moves if m.is_castling]
    assert len(castling_moves) == 0, "Castling should be blocked by knight"


def test_castling_through_check_illegal():
    """Test that castling through check is illegal."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "h1"),
        ("k", "e8"), ("r", "f8"),  # Black rook attacks f1
    ])
    board.turn = Color.WHITE
    board.castling_rights[Color.WHITE]["kingside"] = True
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Should NOT be able to castle (king passes through check)
    castling_moves = [m for m in legal_moves if m.is_castling]
    assert len(castling_moves) == 0, "Cannot castle through check"


def test_castling_from_check_illegal():
    """Test that castling from check is illegal."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "h1"),
        ("k", "e8"), ("r", "e8"),  # Black rook attacks e1
    ])
    board.turn = Color.WHITE
    board.castling_rights[Color.WHITE]["kingside"] = True
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Should NOT be able to castle (king in check)
    castling_moves = [m for m in legal_moves if m.is_castling]
    assert len(castling_moves) == 0, "Cannot castle from check"


def test_castling_rights_lost_after_king_move():
    """Test that castling rights are lost after king moves."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "h1"), ("R", "a1"),
        ("k", "e8"),
    ])
    board.turn = Color.WHITE
    board.castling_rights[Color.WHITE]["kingside"] = True
    board.castling_rights[Color.WHITE]["queenside"] = True
    
    # Move king
    move = Move(0, 4, 0, 5)  # e1-f1
    board.make_move(move)
    
    # Check castling rights are lost
    assert not board.castling_rights[Color.BLACK]["kingside"], "Kingside rights should be lost"
    assert not board.castling_rights[Color.BLACK]["queenside"], "Queenside rights should be lost"


def test_castling_execution():
    """Test that castling moves both king and rook correctly."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "h1"),
        ("k", "e8"),
    ])
    board.turn = Color.WHITE
    board.castling_rights[Color.WHITE]["kingside"] = True
    
    # Perform castling
    castling_move = Move(0, 4, 0, 6, is_castling=True)  # e1-g1
    board.make_move(castling_move)
    
    # Check king moved to g1
    assert board.get_piece(0, 6) is not None, "King should be on g1"
    assert board.get_piece(0, 6).piece_type == PieceType.KING, "Piece on g1 should be king"
    
    # Check rook moved to f1
    assert board.get_piece(0, 5) is not None, "Rook should be on f1"
    assert board.get_piece(0, 5).piece_type == PieceType.ROOK, "Piece on f1 should be rook"
    
    # Check original squares are empty
    assert board.get_piece(0, 4) is None, "e1 should be empty"
    assert board.get_piece(0, 7) is None, "h1 should be empty"


def test_en_passant_legal():
    """Test en passant capture when legal."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("P", "e5"), ("p", "d7"),
    ])
    board.turn = Color.BLACK
    
    # Black makes double pawn push
    move = Move(6, 3, 4, 3)  # d7-d5
    board.make_move(move)
    
    # En passant square should be set
    assert board.en_passant_square == (5, 3), "En passant square should be d6"
    
    # White should be able to capture en passant
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    en_passant_moves = [m for m in legal_moves if m.is_en_passant]
    assert len(en_passant_moves) == 1, "Should have one en passant move"
    assert en_passant_moves[0].to_rank == 5 and en_passant_moves[0].to_file == 3, \
        "En passant should capture to d6"


def test_en_passant_execution():
    """Test that en passant correctly removes the captured pawn."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("P", "e5"), ("p", "d7"),
    ])
    board.turn = Color.BLACK
    
    # Black makes double pawn push
    move = Move(6, 3, 4, 3)  # d7-d5
    board.make_move(move)
    
    # White captures en passant
    en_passant_move = Move(4, 4, 5, 3, captured_piece_type=PieceType.PAWN, is_en_passant=True)
    board.make_move(en_passant_move)
    
    # Check white pawn is on d6
    assert board.get_piece(5, 3) is not None, "White pawn should be on d6"
    assert board.get_piece(5, 3).piece_type == PieceType.PAWN, "Piece on d6 should be pawn"
    assert board.get_piece(5, 3).color == Color.WHITE, "Pawn on d6 should be white"
    
    # Check black pawn on d5 is captured
    assert board.get_piece(4, 3) is None, "d5 should be empty (pawn captured)"


def test_en_passant_expires():
    """Test that en passant opportunity expires after one move."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("P", "e5"), ("p", "d7"), ("p", "h7"),
    ])
    board.turn = Color.BLACK
    
    # Black makes double pawn push
    move = Move(6, 3, 4, 3)  # d7-d5
    board.make_move(move)
    
    # White makes unrelated move
    move = Move(0, 4, 0, 5)  # Ke1-f1
    board.make_move(move)
    
    # En passant square should be cleared
    assert board.en_passant_square is None, "En passant should expire"
    
    # Black makes another move
    move = Move(6, 7, 5, 7)  # h7-h6
    board.make_move(move)
    
    # White should NOT be able to capture en passant anymore
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    en_passant_moves = [m for m in legal_moves if m.is_en_passant]
    assert len(en_passant_moves) == 0, "En passant should have expired"


def test_pawn_promotion_to_queen():
    """Test pawn promotion to queen."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("P", "e7"),  # White pawn ready to promote
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Should have 4 promotion moves (Q, R, B, N)
    promotion_moves = [m for m in legal_moves 
                       if m.from_rank == 6 and m.from_file == 4 
                       and m.promotion_piece_type is not None]
    
    assert len(promotion_moves) == 4, "Should have 4 promotion options"
    
    # Find queen promotion
    queen_promo = [m for m in promotion_moves 
                   if m.promotion_piece_type == PieceType.QUEEN][0]
    
    # Execute promotion
    board.make_move(queen_promo)
    
    # Check pawn became a queen
    promoted_piece = board.get_piece(7, 4)
    assert promoted_piece is not None, "e8 should have a piece"
    assert promoted_piece.piece_type == PieceType.QUEEN, "Promoted piece should be queen"
    assert promoted_piece.color == Color.WHITE, "Promoted piece should be white"


def test_pawn_promotion_by_capture():
    """Test pawn promotion by capturing."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("k", "e8"),
        ("P", "e7"), ("r", "d8"),  # Can promote by capturing rook
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Should be able to promote by capturing
    capture_promotions = [m for m in legal_moves 
                          if m.from_rank == 6 and m.from_file == 4 
                          and m.to_file == 3
                          and m.captured_piece_type == PieceType.ROOK
                          and m.promotion_piece_type is not None]
    
    assert len(capture_promotions) == 4, "Should have 4 promotion options when capturing"
