from pathlib import Path
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

TOKEN: str = os.getenv("DISCORD_TOKEN")
GUILD: str = os.getenv("DISCORD_GUILD")
BLIZZARD_CLIENT_ID: str = os.getenv("BLIZZARD_CLIENT_ID")
BLIZZARD_CLIENT_SECRET: str = os.getenv("BLIZZARD_CLIENT_SECRET")
