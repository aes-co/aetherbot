import os
from pyrogram import Client, filters
from dotenv import load_dotenv


load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

import importlib
import pathlib

def load_plugins():
    plugin_dirs = ["plugins/lookup"]
    for plugin_dir in plugin_dirs:
        for path in pathlib.Path(plugin_dir).glob("*.py"):
            if path.name.startswith("_"):
                continue
            module = f"{plugin_dir.replace('/', '.')}.{path.stem}"
            importlib.import_module(module)

load_plugins()

app = Client("aetherbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("🕵️ Welcome to Aetherbot — OSINT at your fingertips.")

if __name__ == "__main__":
    app.run()
