# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | @NT_BOTS_SUPPORT | LISA-KOREA/UPLOADER-BOT-V4

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/UPLOADER-BOT-V4

import logging
import os
from plugins.config import Config
from pyrogram import Client as Ntbots
from pyrogram import filters

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set the Pyrogram logging level to WARNING to avoid excessive logs
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Main function to start the bot
if __name__ == "__main__":
    # Ensure the download location exists
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    # Set up the plugins directory
    plugins = dict(root="plugins")

    # Initialize the bot client
    Ntbots = Ntbots(
        "URL UPLOADER BOT",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )

    # Print confirmation message
    print("🎊 I AM ALIVE 🎊  • Support @NT_BOTS_SUPPORT")

    # Start the bot and run it
    Ntbots.run()
