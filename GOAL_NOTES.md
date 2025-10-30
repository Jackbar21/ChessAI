# Goal Ideas

These are my initial notes and ideas for achieving each of my three goals:

| Difficulty | Goal | Status |
|-------------|------|--------|
| Easy | Create an agent capable of playing randomized, legal moves | In Progress |
| Medium | Create an agent capable of beating me in a full game of chess | Not Yet Achieved |
| Hard | Create an agent capable of beating Stockfish with knight odds | Not Yet Achieved |

---

## Stage 1: Legal Move Generation

The first goal is to build all the logistics:

- board representation
- move generation
- move validation
- etc.

The aim is to reach a point where I can **play a complete game** against the agent that picks **random legal moves**.

Once that’s achieved:

- Save the **agent code** used for random play.
- Record the **exact game** where the random-move agent played against me.

---

## Stage 2: Building an Engine That Can Beat Me

This phase is all about search and evaluation.

### Search Algorithm

Implement:

- **Minimax / Negamax**
- **Alpha-beta pruning** for efficiency
- **Quiescence search** to reduce the horizon effect
- **Iterative deepening** for more efficiency

### Evaluation Function

Start simple:

```
Pawn = 1
Knight = 3
Bishop = 3
Rook = 5
Queen = 9
King = 200
```

Then gradually enhance with positional heuristics:

- Penalize doubled, isolated, or blocked pawns
- Reward mobility and central control
- Encourage proximity to the opponent king

Reference: [chessprogramming.org/Evaluation](https://www.chessprogramming.org/Evaluation)

When the engine **beats me for the first time**, I’ll record:

- The **evaluation parameters** used
- The **search depth and pruning settings**
- The **exact game** it won

---

## Stage 3: Beating Stockfish

The long-term challenge is to beat Stockfish with **knight odds**.

Initial attempts will likely fail, and that’s where the deeper exploration begins:

- Experimenting with **more advanced heuristics**
- Exploring **neural-network-based evaluation**
- Potentially **rewriting performance-critical parts** in a faster language
- Testing **square-centric** and **bitboard** representations

I may first attempt to beat Stockfish with **queen odds** as an intermediate milestone.

---
