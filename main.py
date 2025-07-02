import asyncio
import logging
from core.client import bot_client
from core.database import connect_db, close_db
from core.config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("aetherbot.log")
    ]
)
log = logging.getLogger(__name__)

async def main():
    log.info("Starting Aetherbot...")
    try:
        await connect_db()
        await bot_client.start()
        log.info("Aetherbot started successfully!")
        await bot_client.idle()
    except Exception as e:
        log.error(f"Error starting Aetherbot: {e}")
    finally:
        await close_db()
        log.info("Aetherbot stopped.")

if __name__ == "__main__":
    asyncio.run(main())