import os, berserk
from dotenv import load_dotenv
from lichess.game import Game


class LichessBot:
    def __init__(self):
        # Load variables from .env
        assert load_dotenv()
        token = os.getenv("LICHESS_API_TOKEN")
        if not token:
            raise ValueError("Missing LICHESS_BOT_TOKEN in .env file")

        session = berserk.TokenSession(token)
        self.client = berserk.Client(session=session)
        assert self.client.account.get()["title"] == "BOT"

    def run(self):
        for event in self.client.bots.stream_incoming_events():
            print(f"\nReceived event: {event}\n`")
            event_type = event["type"]
            if event_type == "challenge":
                event_id = event["challenge"]["id"]
                self.client.bots.accept_challenge(event_id)
            elif event_type == "gameStart":
                game = Game(self.client, event["game"])
                game.start()
