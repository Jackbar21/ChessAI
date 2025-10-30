from abc import ABC, abstractmethod
from src.board import Board
from src.move import Move
from src.movegen import MoveGenerator


class BaseAgent(ABC):
    """Abstract base class for all chess agents."""

    def __init__(self, board: Board):
        self.board = board
        self.move_generator = MoveGenerator(board)
        self.nodes_searched = 0

    @abstractmethod
    def find_best_move(self) -> Move:
        """Return the best move for the current board position."""
        raise NotImplementedError("Must be implemented by subclass")
