"""
Lichess bot connection setup using berserk library.
"""

import os
from dotenv import load_dotenv
import berserk
from src import *

# Load variables from .env
assert load_dotenv()

TOKEN = os.getenv("LICHESS_API_TOKEN")
if not TOKEN:
    raise ValueError("Missing LICHESS_BOT_TOKEN in .env file")

session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)

print("Connected as:", client.account.get())
