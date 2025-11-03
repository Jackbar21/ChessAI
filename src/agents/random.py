from src.agents.base import *
from random import choice as random_choice


class RandomAgent(BaseAgent):
    """
    Chess agent that selects moves randomly.
    """

    def find_best_move(self, depth: int) -> Optional[Move]:
        """
        Find a random legal move for the current position.

        Returns:
            A random legal move, or None if no legal moves (checkmate/stalemate)
        """
        legal_moves = list(self.move_generator.generate_legal_moves())

        if not legal_moves:
            return None  # No legal moves (checkmate or stalemate)

        return random_choice(legal_moves)
