import sys
from pathlib import Path

# Make the project root (one level up from lichess/) available for imports
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lichess.bot import LichessBot

if __name__ == "__main__":
    bot = LichessBot()
    bot.run()
