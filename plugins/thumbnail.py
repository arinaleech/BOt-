import logging
import random
import os
from PIL import Image
import time
from plugins.script import Translation
from pyrogram import Client, filters
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from plugins.functions.help_Nekmo_ffmpeg import take_screen_shot
import shutil
from plugins.functions.forcesub import handle_force_subscribe
from plugins.database.database import db
from plugins.config import Config
from plugins.database.add import add_user_to_database
from plugins.settings.settings import *
import asyncio
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
import logging

# Initialize logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@Client.on_message(filters.photo)
async def save_photo(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you sar :(")
    
    await add_user_to_database(bot, update)

    if Config.UPDATES_CHANNEL:
        fsub = await handle_force_subscribe(bot, update)
        if fsub == 400:
            return

    # Handle photo download and saving
    download_location = os.path.join(Config.DOWNLOAD_LOCATION, f"{update.from_user.id}.jpg")
    try:
        await bot.download_media(message=update, file_name=download_location)
        await db.set_thumbnail(update.from_user.id, thumbnail=update.photo.file_id)
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.SAVED_CUSTOM_THUMB_NAIL,
            reply_to_message_id=update.id
        )
    except Exception as e:
        logger.error(f"Error downloading photo: {e}")
        await update.reply_text("Failed to save the thumbnail.")

@Client.on_message(filters.command(["delthumb"]))
async def delete_thumbnail(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you sar :(")
    
    await add_user_to_database(bot, update)

    if Config.UPDATES_CHANNEL:
        fsub = await handle_force_subscribe(bot, update)
        if fsub == 400:
            return

    download_location = os.path.join(Config.DOWNLOAD_LOCATION, f"{update.from_user.id}.jpg")
    try:
        if os.path.exists(download_location):
            os.remove(download_location)
            await db.set_thumbnail(update.from_user.id, thumbnail=None)
            await bot.send_message(
                chat_id=update.chat.id,
                text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
                reply_to_message_id=update.id
            )
        else:
            await update.reply_text("No thumbnail found to delete.")
    except Exception as e:
        logger.error(f"Error deleting thumbnail: {e}")
        await update.reply_text("An error occurred while deleting the thumbnail.")

@Client.on_message(filters.command("showthumb"))
async def viewthumbnail(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you sar :(")
    
    await add_user_to_database(bot, update)

    if Config.UPDATES_CHANNEL:
        fsub = await handle_force_subscribe(bot, update)
        if fsub == 400:
            return

    thumbnail = await db.get_thumbnail(update.from_user.id)
    if thumbnail:
        await bot.send_photo(
            chat_id=update.chat.id,
            photo=thumbnail,
            caption="Sᴀᴠᴇᴅ Yᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="deleteThumbnail")]]
            ),
            reply_to_message_id=update.id
        )
    else:
        await update.reply_text("No thumbnail found.")

async def Gthumb01(bot, update):
    thumb_image_path = os.path.join(Config.DOWNLOAD_LOCATION, f"{update.from_user.id}.jpg")
    db_thumbnail = await db.get_thumbnail(update.from_user.id)

    if db_thumbnail:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
        try:
            img = Image.open(thumbnail).convert("RGB")
            img = img.resize((100, 100))
            img.save(thumbnail, "JPEG")
        except Exception as e:
            logger.error(f"Error processing thumbnail: {e}")
            thumbnail = None
    else:
        thumbnail = None

    return thumbnail

async def Gthumb02(bot, update, duration, download_directory):
    thumb_image_path = os.path.join(Config.DOWNLOAD_LOCATION, f"{update.from_user.id}.jpg")
    db_thumbnail = await db.get_thumbnail(update.from_user.id)

    if db_thumbnail:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
    else:
        thumbnail = await take_screen_shot(download_directory, os.path.dirname(download_directory), random.randint(0, duration - 1))

    return thumbnail

async def Mdata01(download_directory):
    width, height, duration = 0, 0, 0
    metadata = extractMetadata(createParser(download_directory))

    if metadata:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")

    return width, height, duration

async def Mdata02(download_directory):
    width, duration = 0, 0
    metadata = extractMetadata(createParser(download_directory))

    if metadata:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")

    return width, duration

async def Mdata03(download_directory):
    duration = 0
    metadata = extractMetadata(createParser(download_directory))

    if metadata and metadata.has("duration"):
        duration = metadata.get('duration').seconds

    return duration
