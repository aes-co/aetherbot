from pyrogram import filters
from models.user import User
from core.config import Config

async def is_admin_filter(_, client, message):
    user_id = message.from_user.id
    return user_id in Config.ADMIN_IDS

admin_filter = filters.create(is_admin_filter)

async def is_private_chat_filter(_, client, message):
    return message.chat.type == "private"

private_chat_filter = filters.create(is_private_chat_filter)

async def is_group_chat_filter(_, client, message):
    return message.chat.type in ["group", "supergroup"]

group_chat_filter = filters.create(is_group_chat_filter)