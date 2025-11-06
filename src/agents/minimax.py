import time
from typing import Callable
from src.agents.base import *
from src import Color
from src.agents.transposition import TTEntry, BoundType


class MinimaxAgent(BaseAgent):
    """
    Chess agent using minimax with alpha-beta pruning, quiescence search, iterative deepening, and transposition tables.

    References:
    - [VIDEO] https://youtu.be/l-hh51ncgDI?si=HEflzJDShZmo8rN-
    - Alpha-beta pruning to optimize search: https://www.chessprogramming.org/Alpha-Beta
    - Quiescence search to avoid horizon effect: https://www.chessprogramming.org/Quiescence_Search
    - Iterative deepening: https://www.chessprogramming.org/Iterative_Deepening
    - Transposition tables: https://www.chessprogramming.org/Transposition_Table
    """

    def __init__(self, board: Board):
        super().__init__(board)
        self.start_time = None
        self.time_limit = None
        self.transposition_table = {}  # FEN string -> TTEntry

    def find_best_move(
        self, max_depth: int, time_limit: float = None
    ) -> Optional[Move]:
        """
        Find the best move for the current position.

        Args:
            max_depth: The maximum search depth

        Returns:
            The best move, or None if no legal moves (checkmate/stalemate)
        """
        self.start_time = time.time()
        self.time_limit = time_limit

        best_move = None
        best_value = float("-inf") if self.board.turn == Color.WHITE else float("inf")

        for depth in range(1, max_depth + 1):
            if self._time_exceeded():
                break

            move, value = self._search_at_depth(depth)
            if move is not None:
                best_move, best_value = move, value

        return best_move

    def _search_at_depth(self, max_depth: int) -> Optional[Move]:
        """
        Find the best move for the current position.

        Args:
            max_depth: The maximum search depth

        Returns:
            The best move, or None if no legal moves (checkmate/stalemate)
        """
        alpha, beta = float("-inf"), float("inf")
        legal_moves = self.get_legal_moves()

        # Maximize if white, minimize if black
        is_maximizing = self.board.turn == Color.WHITE
        best_move = legal_moves[0]  # placeholder, not None to assert move found
        best_value = float("-inf") if is_maximizing else float("inf")

        # Base case: no legal moves (checkmate or stalemate)
        if not legal_moves:
            score = 0
            if self.board.is_in_check(self.board.turn):
                score = float("-inf") if is_maximizing else float("inf")
            return None, score

        # Base case: technical draw
        if self.board.is_technical_draw():
            return None, 0

        if is_maximizing:
            for move in legal_moves:
                self.board.make_move(move)
                value = self._minimax(max_depth - 1, alpha, beta, not is_maximizing)
                self.board.unmake_move()

                if value > best_value:
                    best_value = value
                    best_move = move

                alpha = max(alpha, value)
        else:
            for move in legal_moves:
                self.board.make_move(move)
                value = self._minimax(max_depth - 1, alpha, beta, not is_maximizing)
                self.board.unmake_move()

                if value < best_value:
                    best_value = value
                    best_move = move

                beta = min(beta, value)

        return best_move, best_value

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
        original_alpha, original_beta = alpha, beta
        fen = self.board.position_fen()
        entry = self.transposition_table.get(fen, None)
        if entry is not None and entry.depth >= depth:
            if entry.flag == BoundType.EXACT:
                return entry.value
            elif entry.flag == BoundType.LOWERBOUND:
                alpha = max(alpha, entry.value)
            elif entry.flag == BoundType.UPPERBOUND:
                beta = min(beta, entry.value)

            if alpha >= beta:
                return entry.value

        # Setup TT entry
        tt_entry = TTEntry(value=0, depth=depth, flag=BoundType.EXACT, best_move=None)

        # Base case: reached max_depth limit
        if depth <= 0:
            tt_entry.value = self._quiescence_search(alpha, beta, is_maximizing)
        else:
            legal_moves = self.get_legal_moves()
            best_move = legal_moves[0]
            best_value = float("-inf") if is_maximizing else float("inf")

            # 1. No legal moves
            if not legal_moves:
                if self.board.is_in_check(self.board.turn):
                    # Checkmate (-inf for black win, +inf for white win)
                    tt_entry.value = float("-inf") if is_maximizing else float("inf")
                else:
                    # Stalemate
                    tt_entry.value = 0
            # 2. Technical draw
            elif self.board.is_technical_draw():
                tt_entry.value = 0
            # 3. Game continues
            else:
                # PV move first (from transposition table)
                if (
                    fen in self.transposition_table
                    and self.transposition_table[fen].best_move in legal_moves
                ):
                    # Move ordering: put best known move first
                    legal_moves.remove(self.transposition_table[fen].best_move)
                    legal_moves.insert(0, self.transposition_table[fen].best_move)

                for move in legal_moves:
                    self.board.make_move(move)
                    score = self._minimax(depth - 1, alpha, beta, not is_maximizing)
                    self.board.unmake_move()

                    if is_maximizing:
                        if score > best_value:
                            best_value = score
                            best_move = move
                        alpha = max(alpha, score)
                    else:
                        if score < best_value:
                            best_value = score
                            best_move = move
                        beta = min(beta, score)

                    if alpha >= beta:
                        break  # Alpha-beta cutoff

                tt_entry.value = best_value
                tt_entry.best_move = best_move

        # Set TT entry flag
        if tt_entry.value <= original_alpha:
            tt_entry.flag = BoundType.UPPERBOUND
        elif tt_entry.value >= original_beta:
            tt_entry.flag = BoundType.LOWERBOUND
        else:
            tt_entry.flag = BoundType.EXACT
        self.transposition_table[fen] = tt_entry
        return tt_entry.value

    def _quiescence_search(
        self, alpha: float, beta: float, is_maximizing: bool, depth: int = 4
    ) -> float:
        """
        Quiescence search to avoid horizon effect.
        Only searches capture moves to stabilize the position.

        Args:
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player
            depth: Maximum quiescence search depth

        Returns:
            The evaluation score
        """
        cur_eval = self.evaluate_board()

        if depth <= 0:
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
                score = self._quiescence_search(alpha, beta, False, depth - 1)
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
                score = self._quiescence_search(alpha, beta, True, depth - 1)
                self.board.unmake_move()

                if score <= alpha:
                    return alpha
                beta = min(beta, score)

            return beta

    def _time_exceeded(self) -> bool:
        """Check if time limit exceeded."""
        if self.time_limit is None:
            return False
        return (time.time() - self.start_time) >= self.time_limit
