import logging
import os
from pyrogram import Client as Ntbots
from plugins.config import Config

# Logging setup
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Main Bot Initialization
async def main():
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    plugins = dict(root="plugins")

    # Initialize bot with bot_token (no user clients involved)
    bot = Ntbots(
        "Mila_walkar_bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )

    print("🎊 I AM ALIVE 🎊  • Support @NT_BOTS_SUPPORT")
    # Replace bot.idle() with await idle() to keep the bot running
    await bot.start()  # Start the bot
    await bot.idle()  # Await idle to keep bot alive

if __name__ == "__main__":
    import asyncio
    # Run the asynchronous main function
    asyncio.run(main())
