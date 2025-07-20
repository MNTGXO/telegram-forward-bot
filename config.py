import os

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
    DATABASE_PATH = os.getenv("DATABASE_PATH", "forward_bot.db")
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 1))
