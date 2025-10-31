from src.agents.base import *


class MinimaxAgent(BaseAgent):
    """
    Chess agent using minimax with alpha-beta pruning and quiescence search.

    References:
    - [VIDEO] https://youtu.be/l-hh51ncgDI?si=HEflzJDShZmo8rN-
    - Alpha-beta pruning to optimize search: https://www.chessprogramming.org/Alpha-Beta
    - Quiescence search to avoid horizon effect: https://www.chessprogramming.org/Quiescence_Search
    """

    def find_best_move(self, depth: int) -> Optional[Move]:
        """
        Find the best move for the current position.

        Args:
            depth: The search depth

        Returns:
            The best move, or None if no legal moves (checkmate/stalemate)
        """
        best_move = None
        alpha = float("-inf")
        beta = float("inf")

        legal_moves = self.move_generator.generate_legal_moves()

        if not legal_moves:
            return None  # No legal moves (checkmate or stalemate)

        # Maximize if white, minimize if black
        is_maximizing = self.board.turn == Color.WHITE

        if is_maximizing:
            best_value = float("-inf")
            for move in legal_moves:
                self.board.make_move(move)
                value = self._minimax(depth - 1, alpha, beta, False)
                self.board.unmake_move()

                if value > best_value:
                    best_value = value
                    best_move = move

                alpha = max(alpha, value)
        else:
            best_value = float("inf")
            for move in legal_moves:
                self.board.make_move(move)
                value = self._minimax(depth - 1, alpha, beta, True)
                self.board.unmake_move()

                if value < best_value:
                    best_value = value
                    best_move = move

                beta = min(beta, value)

        return best_move

    def _minimax(
        self, depth: int, alpha: float, beta: float, is_maximizing: bool
    ) -> float:
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player, False if minimizing

        Returns:
            The evaluation score for this position
        """

        # Base case: reached depth limit
        if depth <= 0:
            return self._quiescence_search(alpha, beta, is_maximizing)

        # Base case: check for game over
        legal_moves = self.move_generator.generate_legal_moves()
        if not legal_moves:
            if self.board.is_in_check(self.board.turn):
                # Checkmate - very bad for current player
                # Return extreme value based on whose turn it is
                return float("-inf") if is_maximizing else float("inf")
            else:
                # Stalemate
                return 0

        if is_maximizing:
            max_eval = float("-inf")
            for move in legal_moves:
                self.board.make_move(move)
                eval_score = self._minimax(depth - 1, alpha, beta, False)
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
                eval_score = self._minimax(depth - 1, alpha, beta, True)
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
            max_depth: Maximum quiescence depth

        Returns:
            The evaluation score
        """
        cur_eval = self.board.evaluate()

        if max_depth <= 0:
            return cur_eval

        if is_maximizing:
            if cur_eval >= beta:
                return beta
            alpha = max(alpha, cur_eval)

            # Only consider captures
            captures = [
                move
                for move in self.move_generator.generate_legal_moves()
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
                for move in self.move_generator.generate_legal_moves()
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
