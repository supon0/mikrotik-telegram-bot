import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

MIKROTIK_CONFIG = {
    'host': os.getenv("MIKROTIK_HOST"),
    'username': os.getenv("MIKROTIK_USERNAME"),
    'password': os.getenv("MIKROTIK_PASSWORD"),
    'port': int(os.getenv("MIKROTIK_PORT", 8728))
}

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
