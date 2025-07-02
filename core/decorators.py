from functools import wraps
from pyrogram import filters
from core.config import Config
from models.user import User # Akan digunakan setelah models/user.py diisi

def admin_only(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id
        if user_id in Config.ADMIN_IDS:
            return await func(client, message, *args, **kwargs)
        else:
            await message.reply_text("Maaf, perintah ini hanya untuk admin.")
    return wrapper

async def is_registered_filter(_, client, message):
    user_id = message.from_user.id
    user = await User.get_user(user_id)
    return user is not None

registered_user = filters.create(is_registered_filter)