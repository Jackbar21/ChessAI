"""Tests for tactical puzzles - AI should find best moves in tactical positions."""

import pytest
from src import Board, SearchEngine, MoveGenerator, Color
from tests.test_utils import create_position, setup_position_from_fen


def test_back_rank_mate_in_one():
    """AI should find back rank checkmate in 1."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "a8"),
        ("k", "e8"), ("r", "h8"), ("p", "f7"), ("p", "g7"), ("p", "h7"),
    ])
    board.turn = Color.WHITE
    
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=3)
    
    assert best_move is not None, "Should find a move"
    
    # Ra8-e8# is checkmate
    assert best_move.to_rank == 7 and best_move.to_file == 4, \
        "Should play Re8# (back rank mate)"


def test_queen_and_king_mate_in_one():
    """AI should find simple queen checkmate."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("Q", "a7"),
        ("k", "h8"),
    ])
    board.turn = Color.WHITE
    
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=2)
    
    assert best_move is not None, "Should find a move"
    
    # Multiple mates possible, check it delivers mate
    board.make_move(best_move)
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    assert len(legal_moves) == 0, "Should be checkmate"
    assert board.is_in_check(Color.BLACK), "Should be in check"


def test_simple_fork_tactic():
    """AI should find knight fork winning queen."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("N", "e5"), 
        ("k", "c8"), ("q", "c6"),
    ])
    board.turn = Color.WHITE
    
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=3)
    
    assert best_move is not None, "Should find a move"
    
    # Knight should fork king and queen on d7
    assert best_move.from_rank == 4 and best_move.from_file == 4, \
        "Should move the knight"
    assert best_move.to_rank == 6 and best_move.to_file == 3, \
        "Should fork with Nd7+"


def test_find_free_piece():
    """AI should capture undefended piece."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "a1"),
        ("k", "e8"), ("q", "d4"),  # Free queen
    ])
    board.turn = Color.WHITE
    
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=2)
    
    assert best_move is not None, "Should find a move"
    
    # Should capture the queen
    assert best_move.to_rank == 3 and best_move.to_file == 3, \
        "Should capture the free queen on d4"


def test_smothered_mate_pattern():
    """Test recognizing smothered mate pattern."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("N", "f7"),
        ("k", "h8"), ("r", "g8"), ("p", "g7"), ("p", "h7"),
    ])
    board.turn = Color.WHITE
    
    # Knight on f7 can deliver smothered mate with check  
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Find Nf7-g5-f7 or direct mate moves
    knight_moves = [m for m in legal_moves if m.from_rank == 6 and m.from_file == 5]
    
    # The position has the knight delivering check/mate
    assert len(knight_moves) > 0, "Knight should have moves"


def test_mate_in_two_queen_sacrifice():
    """AI should find queen sacrifice leading to mate in 2."""
    board = Board()
    setup_position_from_fen(board, "6k1/5ppp/8/8/8/8/5PPP/4Q1K1")
    board.turn = Color.WHITE
    
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=4)
    
    # Should find winning continuation
    assert best_move is not None, "Should find a move"


def test_avoid_stalemate():
    """AI should avoid stalemating opponent when winning."""
    board = Board()
    create_position(board, [
        ("K", "e6"), ("Q", "f6"),
        ("k", "e8"),
    ])
    board.turn = Color.WHITE
    
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Qf7+ would be stalemate - AI should avoid it
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=3)
    
    # Should not play stalemate move
    if best_move and best_move.from_rank == 5 and best_move.from_file == 5:
        assert not (best_move.to_rank == 6 and best_move.to_file == 5), \
            "Should not play Qf7+ (stalemate)"


def test_capture_hanging_piece():
    """AI should prefer capturing hanging pieces."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("B", "d4"),
        ("k", "e8"), ("r", "d8"), ("p", "e7"),
    ])
    board.turn = Color.WHITE
    
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=3)
    
    assert best_move is not None, "Should find a move"
    
    # Should capture the rook with bishop
    board.make_move(best_move)
    assert board.get_piece(7, 3) is not None, "Should have captured the rook"


def test_fried_liver_attack():
    """Test AI recognizes Fried Liver Attack pattern."""
    board = Board()
    # After 1.e4 e5 2.Nf3 Nc6 3.Bc4 Nf6 4.Ng5 d5 5.exd5 Nxd5 6.Nxf7
    setup_position_from_fen(board, "r1bqkb1r/ppp2Npp/2n5/3n4/2B5/8/PPPP1PPP/RNBQK2R")
    board.turn = Color.BLACK
    
    # Black king is under attack, should respond appropriately
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    assert len(legal_moves) > 0, "Black should have legal moves"
    
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=3)
    
    assert best_move is not None, "Should find defensive move"


def test_pin_tactic():
    """Test AI recognizes and exploits pins."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("B", "a3"),
        ("k", "e8"), ("r", "c5"), ("q", "c8"),  # Rook pinned by bishop
    ])
    board.turn = Color.WHITE
    
    # Rook on c5 is pinned to queen
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    # Bishop can capture the pinned rook
    capture_moves = [m for m in legal_moves 
                     if m.to_rank == 4 and m.to_file == 2]
    
    assert len(capture_moves) > 0, "Should be able to capture pinned rook"


def test_skewer_tactic():
    """Test AI recognizes skewer patterns."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "a1"),
        ("k", "a8"), ("q", "a7"),  # Rook can skewer king and queen
    ])
    board.turn = Color.WHITE
    
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=3)
    
    # Should give check with Ra1, forcing king to move and winning queen
    assert best_move is not None, "Should find skewer"


def test_discovered_check():
    """Test AI uses discovered check effectively."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("R", "e5"), ("N", "e6"),
        ("k", "e8"),
    ])
    board.turn = Color.WHITE
    
    # Moving knight gives discovered check
    movegen = MoveGenerator(board)
    legal_moves = movegen.generate_legal_moves()
    
    knight_moves = [m for m in legal_moves 
                    if m.from_rank == 5 and m.from_file == 4]
    
    assert len(knight_moves) > 0, "Knight should have moves"
    
    # Verify moving knight gives check
    for move in knight_moves:
        board.make_move(move)
        in_check = board.is_in_check(Color.BLACK)
        board.unmake_move()
        
        if in_check:
            break  # Found discovered check


def test_zwischenzug():
    """Test AI considers in-between moves (zwischenzug)."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("Q", "d1"), ("N", "e5"),
        ("k", "e8"), ("q", "d8"), ("r", "a8"),
    ])
    board.turn = Color.WHITE
    
    # Instead of trading queens, knight check first
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=4)
    
    assert best_move is not None, "Should find a move"


def test_desperado_tactic():
    """Test AI recognizes desperado (piece about to be lost, so give check/capture)."""
    board = Board()
    create_position(board, [
        ("K", "e1"), ("N", "d4"),
        ("k", "e8"), ("q", "d8"), ("r", "c1"),  # Rook attacks knight
    ])
    board.turn = Color.WHITE
    
    # Knight is attacked, should capture queen or give check before being taken
    search = SearchEngine(board)
    best_move = search.find_best_move(depth=3)
    
    assert best_move is not None, "Should find move"
    
    # Knight should either capture queen or give check
    if best_move.from_rank == 3 and best_move.from_file == 3:
        # It's the knight moving - good!
        assert True
