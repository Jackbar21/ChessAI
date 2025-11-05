import threading
from src import Board, Move, RandomAgent, MinimaxAgent
from lichess.messages import (
    generate_chat_response,
    GREETINGS,
    generate_game_over_response,
)


class Game(threading.Thread):
    def __init__(self, client, event, **kwargs):
        super().__init__(**kwargs)
        self.game_id = event["id"]
        self.client = client
        self.stream = client.bots.stream_game_state(self.game_id)
        self.current_state = next(self.stream)
        self.color = event["color"]
        self.username = client.account.get()["username"]
        self.opponent_username = event["opponent"]["username"]

        self.board = Board()
        self.board.from_fen(event["fen"])

        # Default to medium difficulty
        self.agent = MinimaxAgent(self.board)
        self.depth = 2

        # Tell user they can change the bot agent at any time via chat
        for greeting in GREETINGS:
            self.client.bots.post_message(
                self.game_id,
                greeting.replace("{{username}}", self.opponent_username),
            )

        if event["isMyTurn"]:
            self.make_move()

    def run(self):
        for event in self.stream:
            print(f"\nReceived game event: {event}\n")
            if event["type"] == "gameState":
                self.handle_state_change(event)
            elif event["type"] == "chatLine":
                self.handle_chat_line(event)

    def handle_chat_line(self, event):
        username = event["username"]
        if username == self.username:
            return  # Ignore own messages

        text = event["text"]
        response = generate_chat_response(username, text)  # Default response

        # Check message for difficulty commands, and override response
        # TODO: Add more difficulty levels later, such as "magnus carlsen" mode
        text_lower = text.lower().strip()
        if text_lower == "easy":
            self.set_easy_mode()
            response = f"Alright {username}, letting you off easy! Switching to Random Agent mode. Don't get too comfy!"
        elif text_lower == "medium":
            self.set_medium_mode()
            response = f"You got it, {username}! Switching to Minimax Agent mode. Time to step up your game!"
        elif text_lower == "hard":
            self.set_hard_mode()
            response = f"Brace yourself, {username}! Switching to Hard Minimax Agent mode. This won't be easy!"

        self.client.bots.post_message(self.game_id, response)

    def set_easy_mode(self):
        self.agent = RandomAgent(self.board)

    def set_medium_mode(self):
        self.agent = MinimaxAgent(self.board)
        self.depth = 2

    def set_hard_mode(self):
        self.agent = MinimaxAgent(self.board)
        self.depth = 4

    def handle_state_change(self, game_state):
        status = game_state["status"]
        if status != "started":
            winner = game_state["winner"] if "winner" in game_state else None
            self.handle_game_over(self.game_id, status, winner)
            return

        time = (
            game_state.get("wtime")
            if self.color == "white"
            else game_state.get("btime")
        )
        inc = (
            game_state.get("winc") if self.color == "white" else game_state.get("binc")
        )

        # Exit early if it's not our turn
        uci_moves = game_state["moves"].split()
        should_move = (len(uci_moves) % 2 == 1 and self.color == "black") or (
            len(uci_moves) % 2 == 0 and self.color == "white"
        )
        if not should_move:
            return

        # Capture opponent's last move
        uci_move = uci_moves[-1]
        assert uci_move is not None, "No moves in game state"
        move = self.board.get_move_from_uci(uci_move)
        self.board.make_move(move)

        # Now agent's turn
        self.make_move()

    def make_move(self):
        agent_move = self.agent.find_best_move(self.depth)
        assert agent_move is not None, "No legal moves available"
        move_str = agent_move.to_uci()
        self.board.make_move(agent_move)
        self.client.bots.make_move(self.game_id, move_str)

    def handle_game_over(self, game_id: str, status: str, winner: str | None) -> str:
        assert status in (
            "aborted",
            "mate",
            "resign",
            "stalemate",
            "timeout",
            "draw",
        ), f"Unknown game status: {status}"

        outcome = status
        if status == "mate":
            outcome = "win" if winner == self.color else "loss"
        elif status == "stalemate":
            outcome = "draw"

        response = generate_game_over_response(self.opponent_username, outcome)
        self.client.bots.post_message(game_id, response)
        return response
