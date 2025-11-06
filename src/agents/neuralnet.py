from src.agents.base import *


class NeuralNetAgent(BaseAgent):
    """
    TODO:
    Chess agent using neural networks for move evaluation.
    This is a placeholder for future implementation, will likely be one
    of the more fun parts of this project to work on.

    Additionally, I can make a Monte Carlo Tree Search (MCTS) agent that
    uses a neural network for position evaluation, similar to AlphaZero.

    This is simply a stub for now, as a reminder to implement later.
    """

    def find_best_move(self, max_depth: int) -> Optional[Move]:
        """
        Find the best move for the current position.

        Args:
            max_depth: The search maximum depth

        Returns:
            The best move, or None if no legal moves (checkmate/stalemate)
        """
        raise NotImplementedError("NeuralNetAgent is not yet implemented")
