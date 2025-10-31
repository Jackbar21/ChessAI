from src.agents.base import *


class NegamaxAgent:
    """
    Chess agent using negamax with alpha-beta pruning and quiescence search.

    References:
    - Negamax:              https://www.chessprogramming.org/Negamax
    - Alpha-beta pruning:   https://www.chessprogramming.org/Alpha-Beta
    - Quiescence search:    https://www.chessprogramming.org/Quies

    NOTE: There is no functional difference between minimax and negamax.
    Negamax is just a more elegant implementation of minimax.
    """

    def find_best_move(self, depth: int) -> Optional[Move]:
        """
        Find the best move for the current position.

        Args:
            depth: The search depth

        Returns:
            The best move, or None if no legal moves (checkmate/stalemate)
        """
        raise NotImplementedError("NegamaxAgent is not yet implemented")
