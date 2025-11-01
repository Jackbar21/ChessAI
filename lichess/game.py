import threading
from src import Board, Move, RandomAgent, MinimaxAgent, NegamaxAgent
from lichess.messages import generate_response, GREETING


class Game(threading.Thread):
    def __init__(self, client, event, **kwargs):
        super().__init__(**kwargs)
        self.game_id = event["id"]
        self.client = client
        self.stream = client.bots.stream_game_state(self.game_id)
        self.current_state = next(self.stream)
        self.username = client.account.get()["username"]
        self.color = event["color"]

        self.board = Board()
        self.board.from_fen(event["fen"])
        self.agent = RandomAgent(self.board)
        self.depth = 4  # Needed for agent

        # Tell user they can change the bot agent at any time via chat
        self.client.bots.post_message(
            self.game_id,
            GREETING.replace("{{username}}", event["opponent"]["username"]),
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
            elif event["type"] == "gameFinish":
                print("Game finished")
                return

    def handle_chat_line(self, event):
        username = event["username"]
        if username == self.username:
            return  # Ignore own messages

        text = event["text"]
        response = generate_response(username, text)  # Default response

        # Check message for agent change commands, and override response
        text_lower = text.lower()
        if "agent=random" in text_lower:
            self.agent = RandomAgent(self.board)
            response = f"Alright {username}, switching to Random Agent mode! Let's see if luck is on your side. 🍀"
        elif "agent=minimax" in text_lower:
            self.agent = MinimaxAgent(self.board)
            response = f"You got it, {username}! Switching to Minimax Agent mode. Prepare to be outsmarted! 🤓"
        elif "agent=negamax" in text_lower:
            self.agent = NegamaxAgent(self.board)
            response = f"Switching to Negamax Agent mode, {username}! Time to bring out the big guns! 💥"

        # TODO: Check message for difficulty commands, and override response
        # E.g. easy might be random agent, medium minimax with alpha-beta, hard negamax with alpha-beta & quiescence search, etc.

        self.client.bots.post_message(self.game_id, response)

    def handle_state_change(self, game_state):
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
        move = Move.from_uci(uci_move)
        self.board.make_move(move)

        # Now agent's turn
        self.make_move()

    def make_move(self):
        agent_move = self.agent.find_best_move(self.depth)
        assert agent_move is not None, "No legal moves available"
        move_str = agent_move.to_uci()
        self.board.make_move(agent_move)
        self.client.bots.make_move(self.game_id, move_str)
