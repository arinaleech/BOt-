import logging
import os
import requests
import time
import math

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Function to detect file size from a URL
def DetectFileSize(url):
    try:
        r = requests.head(url, allow_redirects=True)
        total_size = int(r.headers.get("content-length", 0))
        logger.debug(f"Detected file size: {total_size} bytes")
        return total_size
    except Exception as e:
        logger.error(f"Error detecting file size: {e}")
        return 0

# Function to download a file with progress tracking
def DownLoadFile(url, file_name, chunk_size=1024 * 1024, client=None, ud_type="Downloading", message_id=None, chat_id=None):
    try:
        # Remove the file if it already exists
        if os.path.exists(file_name):
            logger.info(f"File {file_name} already exists. Removing it.")
            os.remove(file_name)

        if not url:
            logger.error("No URL provided for download.")
            return None

        # Initiate download
        r = requests.get(url, allow_redirects=True, stream=True)
        total_size = int(r.headers.get("content-length", 0))
        downloaded_size = 0

        # Download the file in chunks
        with open(file_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    fd.write(chunk)
                    downloaded_size += len(chunk)

                    # Update progress to the client
                    if client is not None and total_size > 0:
                        progress_percentage = (downloaded_size * 100) // total_size
                        try:
                            client.edit_message_text(
                                chat_id,
                                message_id,
                                text=f"{ud_type}: {humanbytes(downloaded_size)} of {humanbytes(total_size)} ({progress_percentage}%)"
                            )
                        except Exception as e:
                            logger.error(f"Error updating progress message: {e}")

        logger.info(f"Download completed: {file_name}")
        return file_name

    except Exception as e:
        logger.error(f"Error in DownLoadFile: {e}")
        return None

# Function to convert bytes to a human-readable format
def humanbytes(size):
    if size == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return f"{s} {size_name[i]}"
