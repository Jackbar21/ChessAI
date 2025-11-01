"""
Lichess bot connection setup using berserk library.
"""

import os
import threading
from dotenv import load_dotenv
import berserk
from src import *
from random import choice as random_choice

FUNNY_RESPONSES = [
    "Bro really said '{{text}}' 🤣",
    "Do you even chess, bro?",
    "Do you think you're funny lil bro?",
    "Bruh look at this dude, username is literally {{username}}. LMFAO.",
    "Is that your move or your life plan? 😂",
    "You call that a strategy? Cute.",
    "Wow… did you learn chess from TikTok?",
    "{{username}}, are you trying to win or just amuse me?",
    "Big brain move… said no one ever.",
    "You might want to google 'how to chess', buddy.",
    "Ok, that was… bold. Very bold. 😎",
    "{{username}} vs logic: 0-1",
    "This game is cute. Keep trying, champ.",
    "Did you forget to move the queen or your common sense?",
    "Bro, even my cat would play better. 🐱",
]


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

        if event["isMyTurn"]:
            self.make_move()

    def run(self):
        for event in self.stream:
            print(f"\nReceived game event: {event}\n")
            if event["type"] == "gameState":
                self.handle_state_change(event)
            elif event["type"] == "chatLine":
                self.handle_chat_line(event)

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

    def handle_chat_line(self, event):
        username = event["username"]
        if username == self.username:
            return  # Ignore own messages

        text = event["text"]
        response = random_choice(FUNNY_RESPONSES)
        response = response.replace("{{username}}", username).replace("{{text}}", text)
        self.client.bots.post_message(self.game_id, response)

    def make_move(self):
        agent_move = self.agent.find_best_move(self.depth)
        assert agent_move is not None, "No legal moves available"
        move_str = agent_move.to_uci()
        self.board.make_move(agent_move)
        self.client.bots.make_move(self.game_id, move_str)


# Load variables from .env
assert load_dotenv()

TOKEN = os.getenv("LICHESS_API_TOKEN")
if not TOKEN:
    raise ValueError("Missing LICHESS_BOT_TOKEN in .env file")

session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)

data = client.account.get()
print("Connected as:", data)
assert data["title"] == "BOT", "The provided token does not belong to a bot account"

# print(client.bots.stream_incoming_events())

is_polite = True
for event in client.bots.stream_incoming_events():
    print(f"\nReceived event: {event}\n`")
    event_type = event["type"]
    if event_type == "challenge":
        event_id = event["challenge"]["id"]
        client.bots.accept_challenge(event_id)
    elif event_type == "gameStart":
        game = Game(client, event["game"])
        game.start()
