from typing import Callable
from src.agents.base import *
from src import Color


class MinimaxAgent(BaseAgent):
    """
    Chess agent using minimax with alpha-beta pruning and quiescence search.

    References:
    - [VIDEO] https://youtu.be/l-hh51ncgDI?si=HEflzJDShZmo8rN-
    - Alpha-beta pruning to optimize search: https://www.chessprogramming.org/Alpha-Beta
    - Quiescence search to avoid horizon effect: https://www.chessprogramming.org/Quiescence_Search
    """

    def __init__(self, board: Board):
        super().__init__(board)

    def find_best_move(self, max_depth: int) -> Optional[Move]:
        """
        Find the best move for the current position.

        Args:
            max_depth: The maximum search depth

        Returns:
            The best move, or None if no legal moves (checkmate/stalemate)
        """
        best_move = None
        alpha = float("-inf")
        beta = float("inf")

        legal_moves = self.get_legal_moves()

        # Base case: no legal moves (checkmate or stalemate)
        if not legal_moves:
            return None

        best_move = legal_moves[0]

        # Base case: technical draw
        if self.board.is_technical_draw():
            return None

        # Maximize if white, minimize if black
        is_maximizing = self.board.turn == Color.WHITE

        if is_maximizing:
            best_value = float("-inf")
            for move in legal_moves:
                self.board.make_move(move)
                value = self._minimax(max_depth - 1, alpha, beta, False)
                self.board.unmake_move()

                if value > best_value:
                    best_value = value
                    best_move = move

                alpha = max(alpha, value)
        else:
            best_value = float("inf")
            for move in legal_moves:
                self.board.make_move(move)
                value = self._minimax(max_depth - 1, alpha, beta, True)
                self.board.unmake_move()

                if value < best_value:
                    best_value = value
                    best_move = move

                beta = min(beta, value)

        return best_move

    def _minimax(
        self, max_depth: int, alpha: float, beta: float, is_maximizing: bool
    ) -> float:
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            max_depth: Remaining search maximum depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player, False if minimizing

        Returns:
            The evaluation score for this position
        """

        # Base case: reached max_depth limit
        if max_depth <= 0:
            return self._quiescence_search(alpha, beta, is_maximizing)

        # Base case: check for game over
        # 1. Technical draw
        if self.board.is_technical_draw():
            return 0
        # 2. No legal moves
        legal_moves = self.get_legal_moves()
        if not legal_moves:
            if self.board.is_in_check(self.board.turn):
                # Checkmate (-inf for black win, +inf for white win)
                return float("-inf") if is_maximizing else float("inf")
            else:
                # Stalemate
                return 0

        if is_maximizing:
            max_eval = float("-inf")
            for move in legal_moves:
                self.board.make_move(move)
                eval_score = self._minimax(max_depth - 1, alpha, beta, False)
                self.board.unmake_move()

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if alpha >= beta:
                    break  # Beta cutoff

            return max_eval
        else:
            min_eval = float("inf")
            for move in legal_moves:
                self.board.make_move(move)
                eval_score = self._minimax(max_depth - 1, alpha, beta, True)
                self.board.unmake_move()

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if alpha >= beta:
                    break  # Alpha cutoff

            return min_eval

    def _quiescence_search(
        self, alpha: float, beta: float, is_maximizing: bool, max_depth: int = 4
    ) -> float:
        """
        Quiescence search to avoid horizon effect.
        Only searches capture moves to stabilize the position.

        Args:
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player
            max_depth: Maximum quiescence search depth

        Returns:
            The evaluation score
        """
        cur_eval = self.evaluate_board()

        if max_depth <= 0:
            return cur_eval

        # Base case: technical draw
        if self.board.is_technical_draw():
            return 0

        # Base case: no legal moves (checkmate or stalemate)
        legal_moves = self.get_legal_moves()
        if not legal_moves:
            if self.board.is_in_check(self.board.turn):
                # Checkmate (-inf for black win, +inf for white win)
                return float("-inf") if is_maximizing else float("inf")
            else:
                # Stalemate
                return 0

        if is_maximizing:
            if cur_eval >= beta:
                return beta
            alpha = max(alpha, cur_eval)

            captures = [
                move
                for move in self.get_legal_moves()
                if move.captured_piece_type is not None
            ]

            for move in captures:
                self.board.make_move(move)
                score = self._quiescence_search(alpha, beta, False, max_depth - 1)
                self.board.unmake_move()

                if score >= beta:
                    return beta
                alpha = max(alpha, score)

            return alpha
        else:
            if cur_eval <= alpha:
                return alpha
            beta = min(beta, cur_eval)

            captures = [
                move
                for move in self.get_legal_moves()
                if move.captured_piece_type is not None
            ]

            for move in captures:
                self.board.make_move(move)
                score = self._quiescence_search(alpha, beta, True, max_depth - 1)
                self.board.unmake_move()

                if score <= alpha:
                    return alpha
                beta = min(beta, score)

            return beta
