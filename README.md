# Chess AI Engine

A fully functional chess engine written in Python.

The goal for this project is to build an engine strong enough to defeat me. My chess rating is between 1400-1800.

I’m using [chessprogramming.org](https://www.chessprogramming.org/) as a major reference and inspiration.

---

## Goals and Progress

| Difficulty | Goal                                                          | Status           |
| ---------- | ------------------------------------------------------------- | ---------------- |
| Easy       | Create an agent capable of playing randomized, legal moves    | Achieved         |
| Medium     | Create an agent capable of beating me in a full game of chess | In Progress      |
| Hard       | Create an agent capable of beating Stockfish with knight odds | Not Yet Achieved |

If you'd like to view my original ideas for tackling these goals, [click here!](GOAL_NOTES.md)

---

## Project Structure

```
ChessAI/
├── src/                   # Main source code
│   ├── __init__.py
│   ├── core/              # Fundamental chess objects
│   │   ├── __init__.py
│   │   ├── board.py
│   │   ├── move.py
│   │   ├── piece.py
│   │   ├── movegen.py
│   │   └── constants.py
│   ├── agents/            # All AI agents
│   │   ├── base.py
│   │   ├── minimax.py
│   │   ├── negamax.py
│   │   ├── random.py
│   │   └── neuralnet.py
│   └── evaluate/          # Evaluation functions
│       ├── evaluate.py
│       ├── material.py
│       ├── pst.py
│       ├── pawn_structure.py
│       ├── mobility.py
│       └── utils.py
├── tests/                 # Testing suite
│   ├── unit/
│   │   ├── test_board_and_movegen.py
│   │   └── test_evaluate.py
│   ├── integration/
│   │   └── test_agent_vs_agent.py
│   └── regression/
│       └── test_known_bugs.py
├── main.py                # Demo script
└── README.md
```

---

## Development Guidelines

- **Branching:** Always create a feature branch from `main` for any new work.
- **Pull Requests:** Only merge via PRs; commits to `main` are prohibited.
- **Commit/PR Prefixes:** Use `[prefix]` style for clarity:
  - `[feature]` – New feature (e.g., `[feature] Add RandomAgent`)
  - `[fix]` – Bug fix
  - `[test]` – Adding or updating tests
  - `[refactor]` – Code refactoring
  - `[docs]` – Documentation
  - `[ci]` – CI/CD updates
- **Squash commits** before merging PRs to keep `main` clean.
- **Delete branch** after merging PR to `main`.

---

## Usage

### Basic Usage

```python
from src import Board, MoveGenerator, MinimaxAgent

# Create a new game
board = Board()
board.setup_initial_position()
print(board)

# Generate legal moves
movegen = MoveGenerator(board)
legal_moves = movegen.generate_legal_moves()
print(f"Legal moves: {[move.to_uci() for move in legal_moves]}")

# Let AI find the best move
agent = MinimaxAgent(board)
best_move = agent.find_best_move(max_depth=2)

# Make the move
if best_move:
    board.make_move(best_move)
    print(board)
```

### Running the Demo

```bash
python3 main.py
```

### Running Tests

```bash
pytest -v
```

---

## License

This is a learning project demonstrating chess engine implementation concepts.
