"""
Chess AI Engine - Main Entry Point

This file demonstrates the basic functionality of the chess engine.
"""

from src import Board, Color, PieceType, evaluate


def main():
    """Main entry point for the chess engine."""
    print("=" * 50)
    print("Chess AI Engine")
    print("=" * 50)
    print()

    # Create a new board and set up the starting position
    board = Board()
    board.setup_initial_position()

    print("Initial Position:")
    print(board)
    print()

    # Display some board information
    print("Board Information:")
    print(f"Turn: {board.turn.name}")
    print(f"Material evaluation: {evaluate(board)}")
    print()

    # Show piece counts
    print(f"White pieces: {len(board.white_pieces)}")
    print(f"Black pieces: {len(board.black_pieces)}")
    print()

    # Test square notation conversion
    print("Testing notation conversion:")
    test_squares = [(0, 0), (0, 4), (7, 4), (3, 3)]
    for rank, file in test_squares:
        notation = board.square_to_notation(rank, file)
        piece = board.get_piece(rank, file)
        piece_str = str(piece) if piece else "empty"
        print(f"  {notation}: {piece_str}")
    print()

    # Show all pieces with their positions
    print("White Pieces:")
    for rank, file, piece in sorted(board.white_pieces):
        notation = board.square_to_notation(rank, file)
        print(f"  {piece.piece_type.name} at {notation}")
    print()

    print("Black Pieces:")
    for rank, file, piece in sorted(board.black_pieces):
        notation = board.square_to_notation(rank, file)
        print(f"  {piece.piece_type.name} at {notation}")
    print()

    print("=" * 50)
    print("Next Steps:")
    print("1. Implement move generation (movegen.py)")
    print("2. Implement make/unmake move functions")
    print("3. Add check detection")
    print("4. Implement search algorithm")
    print("=" * 50)


if __name__ == "__main__":
    main()
