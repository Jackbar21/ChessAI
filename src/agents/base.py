from abc import ABC, abstractmethod
from typing import Optional
from src import Board, Move, MoveGenerator, evaluate


class BaseAgent(ABC):
    """
    Abstract base class for all chess agents.
    All chess agents must implement `find_best_move` method.
    """

    def __init__(self, board: Board):
        self.board = board
        self.move_generator = MoveGenerator(board)

    @abstractmethod
    def find_best_move(self, depth: int) -> Optional[Move]:
        """
        Find the best move for the current position.

        Args:
            depth: The search depth

        Returns:
            The best move, or None if no legal moves (checkmate/stalemate)
        """
        raise NotImplementedError("Must be implemented by subclass")

    def evaluate_board(self) -> int:
        """
        Evaluate the current board position.

        Returns:
            Evaluation score as an integer
        """
        # Default implementation, can be overridden by subclasses
        return evaluate(self.board)
