import logging
import requests
import json
import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.functions.forcesub import handle_force_subscribe
from plugins.functions.display_progress import humanbytes
from plugins.database.add import add_user_to_database
from plugins.functions.ran_text import random_char

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Fallback Translation class (if not provided elsewhere)
class Translation:
    SET_CUSTOM_USERNAME_PASSWORD = "This video is available only for registered users. Please set your username and password."
    FORMAT_SELECTION = "Please select a format:"
    NO_VOID_FORMAT_FOUND = "No valid format found: {}"
    INVALID_URL = "Invalid or unsupported URL provided. Please send a valid link."

# Fallback Config class (if not provided elsewhere)
class Config:
    LOG_CHANNEL = None
    UPDATES_CHANNEL = None
    HTTP_PROXY = ""
    DOWNLOAD_LOCATION = "./downloads"

@Client.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def process_link(bot, update):
    if Config.LOG_CHANNEL:
        try:
            log_message = await update.forward(Config.LOG_CHANNEL)
            log_info = f"Message Sender Information\n\n"
            log_info += f"First Name: {update.from_user.first_name}\n"
            log_info += f"User ID: {update.from_user.id}\n"
            log_info += f"Username: @{update.from_user.username}" if update.from_user.username else ""
            log_info += f"\nUser Link: {update.from_user.mention}"
            await log_message.reply_text(
                text=log_info,
                disable_web_page_preview=True,
                quote=True
            )
        except Exception as error:
            logger.error(f"Error logging message: {error}")

    if not update.from_user:
        return await update.reply_text("I don't know about you, sir 😅")

    await add_user_to_database(bot, update)

    if Config.UPDATES_CHANNEL:
        fsub = await handle_force_subscribe(bot, update)
        if fsub == 400:
            return

    url = update.text
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None

    # Parse URL and optional parameters
    if "|" in url:
        parts = url.split("|")
        url = parts[0].strip()
        file_name = parts[1].strip() if len(parts) > 1 else None
        if len(parts) == 4:
            youtube_dl_username = parts[2].strip()
            youtube_dl_password = parts[3].strip()

    if not url.startswith("http"):
        await update.reply_text(Translation.INVALID_URL, reply_to_message_id=update.id)
        return

    # yt-dlp command preparation
    command_to_exec = [
        "yt-dlp", "--no-warnings", "--youtube-skip-hls-manifest", "-j", url
    ]

    if Config.HTTP_PROXY:
        command_to_exec.extend(["--proxy", Config.HTTP_PROXY])

    if "instagram.com" in url:
        command_to_exec.extend(["--merge-output-format", "mp4"])

    if youtube_dl_username:
        command_to_exec.extend(["--username", youtube_dl_username])

    if youtube_dl_password:
        command_to_exec.extend(["--password", youtube_dl_password])

    logger.info(f"Command to execute: {' '.join(command_to_exec)}")

    # Notify the user
    chk = await bot.send_message(
        chat_id=update.chat.id,
        text="🔄 Processing your link. Please wait...",
        disable_web_page_preview=True,
        reply_to_message_id=update.id,
        parse_mode=enums.ParseMode.HTML
    )

    # Run yt-dlp
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    error_response = stderr.decode().strip()
    output_response = stdout.decode().strip()

    if error_response:
        logger.error(f"Error from yt-dlp: {error_response}")
        await chk.delete()
        await bot.send_message(
            chat_id=update.chat.id,
            text=f"❌ Error occurred while processing your request:\n\n<code>{error_response}</code>",
            reply_to_message_id=update.id,
            parse_mode=enums.ParseMode.HTML
        )
        return

    if not output_response:
        await chk.delete()
        await bot.send_message(
            chat_id=update.chat.id,
            text="❌ No response from yt-dlp. Please try again later.",
            reply_to_message_id=update.id
        )
        return

    try:
        response_json = json.loads(output_response)
    except json.JSONDecodeError:
        await chk.delete()
        await bot.send_message(
            chat_id=update.chat.id,
            text="❌ Failed to parse yt-dlp response. Please try again later.",
            reply_to_message_id=update.id
        )
        return

    # Prepare buttons for format selection
    inline_keyboard = []
    duration = response_json.get("duration")
    randem = random_char(5)
    if "formats" in response_json:
        for formats in response_json["formats"]:
            format_id = formats.get("format_id")
            format_note = formats.get("format_note", formats.get("format", "Unknown"))
            format_ext = formats.get("ext", "Unknown")
            approx_file_size = humanbytes(formats["filesize"]) if formats.get("filesize") else "Unknown size"

            if "audio only" not in format_note:
                cb_string_video = f"video|{format_id}|{format_ext}|{randem}"[:64]
                inline_keyboard.append([
                    InlineKeyboardButton(
                        f"🎬 {format_note} {format_ext} ({approx_file_size})",
                        callback_data=cb_string_video.encode("UTF-8")
                    )
                ])

        if duration:
            cb_string_64 = f"audio|64k|mp3|{randem}"
            cb_string_128 = f"audio|128k|mp3|{randem}"
            cb_string_320 = f"audio|320k|mp3|{randem}"
            inline_keyboard.append([
                InlineKeyboardButton("🎵 MP3 (64 kbps)", callback_data=cb_string_64.encode("UTF-8")),
                InlineKeyboardButton("🎵 MP3 (128 kbps)", callback_data=cb_string_128.encode("UTF-8"))
            ])
            inline_keyboard.append([
                InlineKeyboardButton("🎵 MP3 (320 kbps)", callback_data=cb_string_320.encode("UTF-8"))
            ])

        inline_keyboard.append([
            InlineKeyboardButton("⛔ Close", callback_data="close")
        ])

    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await chk.delete()
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.FORMAT_SELECTION,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )
