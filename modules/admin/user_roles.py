from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from core.decorators import admin_only
from models.user import User
from core.database import get_database

log = logging.getLogger(__name__)

@Client.on_message(filters.command("listadmins") & filters.private & admin_only)
async def list_admins_command(client: Client, message: Message):
    """
    Lists all users currently marked as administrators in the bot's database.
    Usage: /listadmins
    """
    db = get_database()
    
    # Fetch all users who are marked as admin
    admin_users_data = await db[User.COLLECTION_NAME].find({"is_admin": True}).to_list(length=None)

    if not admin_users_data:
        await message.reply_text("No administrators are currently registered in the database.")
        return

    admin_list_text = "**Current Administrators:**\n\n"
    for user_data in admin_users_data:
        user_id = user_data.get('user_id')
        username = user_data.get('username', 'N/A')
        first_name = user_data.get('first_name', 'N/A')
        admin_list_text += f"- **{first_name}** (`{user_id}`) @{username}\n"
    
    await message.reply_text(admin_list_text)
    log.info(f"Admin {message.from_user.id} requested list of administrators.")

# Note: The /setadmin and /removeadmin commands are already implemented
# in handlers/command_handlers.py for convenience, as they are core admin functions.
# If you prefer strict modularity, you could move them here.
