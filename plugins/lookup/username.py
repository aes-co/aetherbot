from pyrogram import Client, filters
from pyrogram.types import Message
import httpx

PLATFORMS = {
    "GitHub": "https://github.com/{username}",
    "Reddit": "https://www.reddit.com/user/{username}",
    "Instagram": "https://www.instagram.com/{username}",
    "TikTok": "https://www.tiktok.com/@{username}",
    "Twitter (X)": "https://x.com/{username}",
    "Pinterest": "https://www.pinterest.com/{username}",
    "Steam": "https://steamcommunity.com/id/{username}",
    "Keybase": "https://keybase.io/{username}",
}


async def check_profile(url: str) -> bool:
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            res = await client.get(url)
            return res.status_code == 200
    except Exception:
        return False


@Client.on_message(filters.command("osint") & filters.private)
async def osint_username(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("🔍 Gunakan format: `/osint <username>`", quote=True)

    username = message.text.split(maxsplit=1)[1]
    await message.reply_text(f"⏳ Mencari jejak `{username}` di internet...", quote=True)

    found = []
    for name, template in PLATFORMS.items():
        url = template.format(username=username)
        exists = await check_profile(url)
        if exists:
            found.append(f"✅ **{name}**: [link]({url})")

    if not found:
        return await message.reply_text(f"❌ Tidak ditemukan profil untuk `{username}`.")

    result = "\n".join(found)
    await message.reply_text(f"**Hasil pencarian untuk:** `{username}`\n\n{result}", disable_web_page_preview=True)
