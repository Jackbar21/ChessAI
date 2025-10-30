# Chess AI Engine

A fully functional chess engine written in Python.  

The goal for this project is to build an engine strong enough to defeat me. My chess rating is between 1400-1800.

I’m using [chessprogramming.org](https://www.chessprogramming.org/) as a major reference and inspiration.

---

## Goals and Progress

| Difficulty | Goal | Status |
|-------------|------|--------|
| Easy | Create an agent capable of playing randomized, legal moves | In Progress |
| Medium | Create an agent capable of beating me in a full game of chess | Not Yet Achieved |
| Hard | Create an agent capable of beating Stockfish with knight odds | Not Yet Achieved |

If you'd like to view my original ideas for tackling these goals, [click here!](GOAL_NOTES.md)

---

## Project Structure

```
ChessAI/
├── src/
│   ├── __init__.py       # Package exports
│   ├── constants.py      # Enums and constants
│   ├── piece.py          # Piece representation
│   ├── board.py          # Board state and operations
│   ├── move.py           # Move representation
│   ├── movegen.py        # Move generation engine
│   └── search.py         # AI search algorithm
├── main.py               # Demo script
├── test_chess.py         # Comprehensive test suite
└── README.md
```

## Usage

### Basic Usage

```python
from src import Board, MoveGenerator, SearchEngine

# Create a new game
board = Board()
board.setup_initial_position()

# Generate legal moves
movegen = MoveGenerator(board)
legal_moves = movegen.generate_legal_moves()

# Let AI find the best move
search = SearchEngine(board)
best_move = search.find_best_move(depth=4)

# Make the move
if best_move:
    board.make_move(best_move)
    print(board.display())
```

### Running the Demo

```bash
python3 main.py
```

### Running Tests

```bash
pytest -v
```

## License

This is a learning project demonstrating chess engine implementation concepts.
