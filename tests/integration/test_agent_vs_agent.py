import pytest
from src import Board, MoveGenerator, BaseAgent, RandomAgent


@pytest.mark.parametrize("MoveAgent", [RandomAgent])
@pytest.mark.slow
def test_agent_vs_self(MoveAgent: type[BaseAgent]):
    """
    Test RandomAgent's ability to select a legal move.
    Continues making random moves until checkmate/stalemate.
    """
    board = Board()
    board.setup_initial_position()
    agent = MoveAgent(board)

    move_count = 0
    while not board.is_game_over():
        move = agent.find_best_move(depth=1)
        board.make_move(move)
        move_count += 1

    print(f"Game over after {move_count} moves.")
    print(board)
    assert board.is_game_over(), "The game should be over"
