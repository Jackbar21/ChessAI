from enum import Enum


class COLOR(Enum):
    BLACK = 0
    WHITE = 1


class PIECE_TYPE(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5


class SQUARE(Enum):
    A1 = 0
    A2 = 1
    A3 = 2
    A4 = 3
    A5 = 4
    A6 = 5
    A7 = 6
    A8 = 7
    B1 = 8
    B2 = 9
    B3 = 10
    B4 = 11
    B5 = 12
    B6 = 13
    B7 = 14
    B8 = 15
    C1 = 16
    C2 = 17
    C3 = 18
    C4 = 19
    C5 = 20
    C6 = 21
    C7 = 22
    C8 = 23
    D1 = 24
    D2 = 25
    D3 = 26
    D4 = 27
    D5 = 28
    D6 = 29
    D7 = 30
    D8 = 31
    E1 = 32
    E2 = 33
    E3 = 34
    E4 = 35
    E5 = 36
    E6 = 37
    E7 = 38
    E8 = 39
    F1 = 40
    F2 = 41
    F3 = 42
    F4 = 43
    F5 = 44
    F6 = 45
    F7 = 46
    F8 = 47
    G1 = 48
    G2 = 49
    G3 = 50
    G4 = 51
    G5 = 52
    G6 = 53
    G7 = 54
    G8 = 55
    H1 = 56
    H2 = 57
    H3 = 58
    H4 = 59
    H5 = 60
    H6 = 61
    H7 = 62
    H8 = 63


def get_piece_value(piece_type: PIECE_TYPE) -> int:
    return {
        PIECE_TYPE.PAWN: 1,
        PIECE_TYPE.KNIGHT: 3,
        PIECE_TYPE.BISHOP: 3,
        PIECE_TYPE.ROOK: 5,
        PIECE_TYPE.QUEEN: 9,
        PIECE_TYPE.KING: 200,
    }[piece_type]


class Piece:
    def __init__(self, piece_type: PIECE_TYPE, color: COLOR, square: SQUARE):
        self.piece_type = piece_type
        self.color = color
        self.square = square
        self.value = get_piece_value(piece_type)
        self.position = (square.value // 8, square.value % 8)

    def set_position(self, x: int, y: int):
        self.position = (x, y)

    def get_position(self):
        return self.position


class Board:
    def __init__(self):
        self.pieces = []

    def add_piece(self, piece: Piece):
        self.pieces.append(piece)

    def get_pieces(self):
        return self.pieces


def initialize_game():
    board = Board()

    # White pieces
    board.add_piece(Piece(PIECE_TYPE.ROOK, COLOR.WHITE, SQUARE.A1))
    board.add_piece(Piece(PIECE_TYPE.KNIGHT, COLOR.WHITE, SQUARE.B1))
    board.add_piece(Piece(PIECE_TYPE.BISHOP, COLOR.WHITE, SQUARE.C1))
    board.add_piece(Piece(PIECE_TYPE.QUEEN, COLOR.WHITE, SQUARE.D1))
    board.add_piece(Piece(PIECE_TYPE.KING, COLOR.WHITE, SQUARE.E1))
    board.add_piece(Piece(PIECE_TYPE.BISHOP, COLOR.WHITE, SQUARE.F1))
    board.add_piece(Piece(PIECE_TYPE.KNIGHT, COLOR.WHITE, SQUARE.G1))
    board.add_piece(Piece(PIECE_TYPE.ROOK, COLOR.WHITE, SQUARE.H1))

    # Black pieces
    board.add_piece(Piece(PIECE_TYPE.ROOK, COLOR.BLACK, SQUARE.A8))
    board.add_piece(Piece(PIECE_TYPE.KNIGHT, COLOR.BLACK, SQUARE.B8))
    board.add_piece(Piece(PIECE_TYPE.BISHOP, COLOR.BLACK, SQUARE.C8))
    board.add_piece(Piece(PIECE_TYPE.QUEEN, COLOR.BLACK, SQUARE.D8))
    board.add_piece(Piece(PIECE_TYPE.KING, COLOR.BLACK, SQUARE.E8))
    board.add_piece(Piece(PIECE_TYPE.BISHOP, COLOR.BLACK, SQUARE.F8))
    board.add_piece(Piece(PIECE_TYPE.KNIGHT, COLOR.BLACK, SQUARE.G8))
    board.add_piece(Piece(PIECE_TYPE.ROOK, COLOR.BLACK, SQUARE.H8))

    # Pawns
    for i in range(8):
        board.add_piece(Piece(PIECE_TYPE.PAWN, COLOR.WHITE, SQUARE(i * 8 + 1)))
        board.add_piece(Piece(PIECE_TYPE.PAWN, COLOR.BLACK, SQUARE(i * 8 + 6)))

    # Add pieces to the board as needed
    return board


if __name__ == "__main__":
    # Example usage
    print(f"Value of a Knight: {get_piece_value(PIECE_TYPE.KNIGHT)}")
    print(f"Color of BLACK: {COLOR.BLACK}")
    board = initialize_game()
    for piece in board.get_pieces():
        if piece.piece_type == PIECE_TYPE.PAWN and piece.color == COLOR.BLACK:
            print(
                f"{piece.color.name} {piece.piece_type.name} at {piece.square.name} with value {piece.value}"
            )
