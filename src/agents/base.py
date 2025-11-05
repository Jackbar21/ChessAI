from abc import ABC, abstractmethod
from typing import List, Optional
from src import Board, Move, MoveGenerator
from src.evaluate.evaluate import evaluate
from .utils import evaluate_move


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

    def get_legal_moves(self) -> List[Move]:
        """
        Get a sorted list of legal moves for the current position.

        Returns:
            List of legal Move objects, sorted by their evaluation score
        """
        legal_moves = self.move_generator.generate_legal_moves()
        legal_moves.sort(key=evaluate_move, reverse=True)
        return legal_moves
