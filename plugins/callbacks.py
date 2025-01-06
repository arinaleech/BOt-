import os
import logging
from pyrogram import Client, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes
from plugins.config import Config
from plugins.dl_button import ddl_call_back
from plugins.button import youtube_dl_call_back
from plugins.settings.settings import OpenSettings
from script import Translation 
from plugins.database.database import db

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@Client.on_callback_query()
async def button(bot, update):
    try:
        if update.data == "home":
            await update.message.edit_text(
                text=script.START_TEXT.format(update.from_user.mention),
                reply_markup=Translation.START_BUTTONS,
                disable_web_page_preview=True
            )
        elif update.data == "help":
            await update.message.edit_text(
                text=script.HELP_TEXT,
                reply_markup=script.HELP_BUTTONS,
                disable_web_page_preview=True
            )
        elif update.data == "about":
            await update.message.edit_text(
                text=script.ABOUT_TEXT,
                reply_markup=script.ABOUT_BUTTONS,
                disable_web_page_preview=True
            )
        elif update.data == "OpenSettings":
            await update.answer()
            await OpenSettings(update.message)
        elif update.data == "showThumbnail":
            thumbnail = await db.get_thumbnail(update.from_user.id)
            if not thumbnail:
                await update.answer("You didn't set any custom thumbnail!", show_alert=True)
            else:
                await update.answer()
                await bot.send_photo(
                    chat_id=update.message.chat.id,
                    photo=thumbnail,
                    caption="Custom Thumbnail",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Delete Thumbnail", callback_data="deleteThumbnail")]]
                    )
                )
        elif update.data == "deleteThumbnail":
            await db.set_thumbnail(update.from_user.id, None)
            await update.answer("Custom thumbnail deleted. Default thumbnail will be used now.", show_alert=True)
            await update.message.delete()
        elif update.data == "setThumbnail":
            await update.message.edit_text(
                text=Translation.TEXT,
                reply_markup=script.BUTTONS,
                disable_web_page_preview=True
            )
        elif update.data == "triggerUploadMode":
            await update.answer()
            upload_as_doc = await db.get_upload_as_doc(update.from_user.id)
            await db.set_upload_as_doc(update.from_user.id, not upload_as_doc)
            await OpenSettings(update.message)
        elif "close" in update.data:
            await update.message.delete()
        elif "|" in update.data:
            await youtube_dl_call_back(bot, update)
        elif "=" in update.data:
            await ddl_call_back(bot, update)
        else:
            await update.message.delete()
    except Exception as e:
        logger.error(f"Error in callback query: {e}")
