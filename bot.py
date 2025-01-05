import logging
import os
from pyrogram import Client, filters
from plugins.config import Config
from pyrogram import idle

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bot client setup
bot = Client(
    "Mila_walkar_bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    plugins=dict(root="plugins")
)

# Main logic to start the bot
if __name__ == "__main__":
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    bot.start()
    print("🎊 I AM ALIVE 🎊  • Support @NT_BOTS_SUPPORT")
  
    # Idle to keep the bot running
    try:
        idle()
    except KeyboardInterrupt:
        print("Bot is shutting down...")

    bot.stop()
