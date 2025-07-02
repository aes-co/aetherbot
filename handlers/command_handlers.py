from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from core.decorators import admin_filter
from models.user import User # Untuk register user

log = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    user = await User.get_user(user_id)
    if not user:
        user = User(user_id=user_id, username=username, first_name=first_name)
        await user.save()
        await message.reply_text(
            f"Halo {first_name}! Selamat datang di Aetherbot, bot OSINT dan Investigasi Anda."
            f"\nSaya telah mendaftarkan Anda. Gunakan /help untuk melihat perintah yang tersedia."
        )
        log.info(f"New user registered: {user_id} ({username})")
    else:
        await message.reply_text(
            f"Selamat datang kembali, {first_name}! Gunakan /help untuk melihat perintah yang tersedia."
        )

@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    help_text = (
        "**Daftar Perintah Aetherbot:**\n\n"
        "**OSINT:**\n"
        "`/userinfo <username_atau_id>` - Mendapatkan info publik pengguna Telegram.\n"
        "`/channelinfo <username_atau_id>` - Mendapatkan info publik channel/grup Telegram.\n"
        "`/analyze_link <url>` - Menganalisis tautan untuk potensi ancaman.\n"
        "`/reverse_image <reply_to_photo>` - Melakukan pencarian gambar terbalik.\n\n"
        "**Investigasi:**\n"
        "`/newcase <judul_kasus>` - Membuat kasus investigasi baru.\n"
        "`/add_evidence <case_id> <reply_to_message>` - Menambahkan pesan/media sebagai bukti ke kasus.\n"
        "`/listcases` - Melihat daftar kasus Anda.\n"
        "`/viewcase <case_id>` - Melihat detail dan bukti dalam kasus.\n"
        "`/report <case_id>` - Menghasilkan laporan untuk kasus.\n\n"
        "**Admin (jika Anda admin):**\n"
        "`/setadmin <user_id>` - Mengatur pengguna sebagai admin.\n"
        "`/removeadmin <user_id>` - Menghapus pengguna dari admin.\n"
        "`/monitor_keyword <keyword>` - Memulai pemantauan kata kunci di grup publik.\n\n"
        "**Lain-lain:**\n"
        "`/help` - Menampilkan pesan bantuan ini.\n"
    )
    await message.reply_text(help_text)

@Client.on_message(filters.command("setadmin") & admin_filter)
async def set_admin_command(client: Client, message: Message):
    args = message.command
    if len(args) < 2 or not args[1].isdigit():
        await message.reply_text("Penggunaan: `/setadmin <user_id>`")
        return

    target_user_id = int(args[1])
    user = await User.get_user(target_user_id)
    if user:
        if user.is_admin:
            await message.reply_text(f"Pengguna {target_user_id} sudah menjadi admin.")
        else:
            user.is_admin = True
            await user.save()
            await message.reply_text(f"Pengguna {target_user_id} sekarang adalah admin.")
    else:
        # Jika user belum terdaftar, daftarkan dan set sebagai admin
        new_admin_user = User(user_id=target_user_id, is_admin=True, username="unknown", first_name="unknown")
        await new_admin_user.save()
        await message.reply_text(f"Pengguna {target_user_id} telah didaftarkan dan diatur sebagai admin.")
    log.info(f"Admin status set for {target_user_id} by {message.from_user.id}")

@Client.on_message(filters.command("removeadmin") & admin_filter)
async def remove_admin_command(client: Client, message: Message):
    args = message.command
    if len(args) < 2 or not args[1].isdigit():
        await message.reply_text("Penggunaan: `/removeadmin <user_id>`")
        return

    target_user_id = int(args[1])
    user = await User.get_user(target_user_id)
    if user:
        if not user.is_admin:
            await message.reply_text(f"Pengguna {target_user_id} bukan admin.")
        else:
            user.is_admin = False
            await user.save()
            await message.reply_text(f"Pengguna {target_user_id} telah dihapus dari admin.")
    else:
        await message.reply_text(f"Pengguna {target_user_id} tidak ditemukan di database.")
    log.info(f"Admin status removed for {target_user_id} by {message.from_user.id}")