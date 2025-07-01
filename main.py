from pyrogram import Client, filters
import os
from dotenv import load_dotenv

load_dotenv()

app = Client(
    "aetherbot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("🕵️‍♂️ Welcome to Aetherbot! Let's investigate.")

app.run()
