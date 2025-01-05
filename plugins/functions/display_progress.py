import time
import math
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums

# A function to track and display progress for Pyrogram
async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start,
    bar_width=20,
    status=""
):
    now = time.time()
    diff = now - start
    percentage = current * 100 / total
    speed = current / diff if diff > 0 else 0
    elapsed_time = round(diff) * 1000
    time_to_completion = round((total - current) / speed) * 1000 if speed > 0 else 0
    estimated_total_time = elapsed_time + time_to_completion

    elapsed_time_str = TimeFormatter(milliseconds=elapsed_time)
    estimated_total_time_str = TimeFormatter(milliseconds=estimated_total_time)

    # Create a progress bar
    filled_length = math.floor(percentage / (100 / bar_width))
    progress_bar = ''.join(["█" for _ in range(filled_length)]) + \
                   ''.join(["░" for _ in range(bar_width - filled_length)])

    # Generate progress display text
    tmp = (
        f"**Progress**: {round(percentage, 2)}%\n"
        f"**[{progress_bar}]**\n"
        f"**Uploaded**: {humanbytes(current)} of {humanbytes(total)}\n"
        f"**Speed**: {humanbytes(speed)}/s\n"
        f"**Elapsed**: {elapsed_time_str}\n"
        f"**ETA**: {estimated_total_time_str if estimated_total_time_str != '' else '0 s'}"
    )

    # Add user-defined status and type of upload/download
    status_message = f"**{ud_type}**\n\n{status}\n\n{tmp}"

    # Try to update the progress message
    try:
        await message.edit(
            text=status_message,
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('⛔️ Cancel', callback_data='close')]
                ]
            )
        )
    except Exception as e:
        print(f"Error updating progress: {e}")

# Convert bytes into a human-readable format
def humanbytes(size):
    if not size:
        return "0 B"
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size >= power and n < len(Dic_powerN) - 1:
        size /= power
        n += 1
    return f"{round(size, 2)} {Dic_powerN[n]}"

# Convert milliseconds into a human-readable time format
def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0:
        parts.append(f"{seconds}s")
    if milliseconds > 0:
        parts.append(f"{milliseconds}ms")

    return ', '.join(parts) if parts else "0s"
