"""
Search algorithm for finding the best chess move.

Implements negamax with alpha-beta pruning (TODO: and quiescence search).
- Negamax is more elegant minimax implementation: https://www.chessprogramming.org/Negamax
- Alpha-beta pruning to optimize search: https://www.chessprogramming.org/Alpha-Beta
- Quiescence search to avoid horizon effect: https://www.chessprogramming.org/Quiescence_Search
"""

from typing import Optional
from src.board import Board
from src.move import Move
from src.movegen import MoveGenerator


class SearchEngine:
    """Chess search engine using negamax with alpha-beta pruning."""

    def __init__(self, board: Board):
        """
        Initialize the search engine.

        Args:
            board: The Board instance to search on
        """
        self.board = board
        self.move_generator = MoveGenerator(board)
        self.nodes_searched = 0

    def find_best_move(self, depth: int = 4) -> Optional[Move]:
        """
        Find the best move for the current position using negamax.

        Args:
            depth: The search depth (default 4)

        Returns:
            The best move, or None if no legal moves
        """
        self.nodes_searched = 0
        best_move = None
        best_value = float("-inf")

        legal_moves = self.move_generator.generate_legal_moves()
        if not legal_moves:
            return None

        alpha = float("-inf")
        beta = float("inf")

        for move in legal_moves:
            self.board.make_move(move)
            value = -self._negamax(depth - 1, -beta, -alpha)
            self.board.unmake_move()

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, value)

        return best_move

    def _negamax(self, depth: int, alpha: float, beta: float) -> float:
        """
        Negamax search with alpha-beta pruning.

        Args:
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning

        Returns:
            Evaluation score for current position
        """
        self.nodes_searched += 1

        legal_moves = self.move_generator.generate_legal_moves()

        # Terminal node handling
        if depth <= 0 or not legal_moves:
            # TODO: Implement quiescence search
            return self.board.evaluate()

        max_eval = float("-inf")

        for move in legal_moves:
            self.board.make_move(move)
            eval_score = -self._negamax(depth - 1, -beta, -alpha)
            self.board.unmake_move()

            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)

            if alpha >= beta:
                break  # Beta cutoff

        return max_eval

    def get_stats(self) -> str:
        """Get search statistics."""
        return f"Nodes searched: {self.nodes_searched:,}"
