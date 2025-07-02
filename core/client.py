from pyrogram import Client
from core.config import Config

bot_client = Client(
    "aetherbot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="modules")
)