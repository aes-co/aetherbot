import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MONGO_URI = os.getenv("MONGO_URI")
    LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(',')))

    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
    HUNTER_IO_API_KEY = os.getenv("HUNTER_IO_API_KEY", "")
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
    HAVEIBEENPWNED_API_KEY = os.getenv("HAVEIBEENPWNED_API_KEY", "")