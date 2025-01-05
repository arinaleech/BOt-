import logging
import asyncio
import os
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Check FFmpeg availability
if not shutil.which("ffmpeg"):
    raise EnvironmentError("FFmpeg is not installed or not in PATH. Please install FFmpeg to proceed.")


# Function to add a watermark to a video or image
async def place_water_mark(input_file, output_file, water_mark_file):
    try:
        metadata = extractMetadata(createParser(input_file))
        if not metadata or not metadata.has("width"):
            raise ValueError("Unable to extract video width from metadata.")

        width = metadata.get("width")
        watermarked_file = output_file + ".watermark.png"

        # Command to scale the watermark
        scale_command = [
            "ffmpeg", "-i", water_mark_file,
            "-y", "-v", "quiet", "-vf",
            f"scale={width}*0.5:-1",
            watermarked_file
        ]
        await run_command(scale_command)

        # Command to overlay the watermark on the video/image
        overlay_command = [
            "ffmpeg", "-i", input_file, "-i", watermarked_file,
            "-filter_complex", "overlay=(main_w-overlay_w):(main_h-overlay_h)",
            output_file
        ]
        await run_command(overlay_command)

        return output_file
    except Exception as e:
        logger.error(f"Error in place_water_mark: {e}")
        raise


# Function to take a screenshot from a video
async def take_screen_shot(video_file, output_directory, ttl):
    try:
        output_file = os.path.join(output_directory, f"{time.time()}.jpg")
        command = [
            "ffmpeg", "-ss", str(ttl),
            "-i", video_file,
            "-vframes", "1",
            output_file
        ]
        await run_command(command)

        if os.path.exists(output_file):
            return output_file
        else:
            raise FileNotFoundError(f"Screenshot not created: {output_file}")
    except Exception as e:
        logger.error(f"Error in take_screen_shot: {e}")
        raise


# Function to create a shorter video clip
async def cult_small_video(video_file, output_directory, start_time, end_time):
    try:
        output_file = os.path.join(output_directory, f"{round(time.time())}.mp4")
        command = [
            "ffmpeg", "-i", video_file,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-async", "1", "-strict", "-2",
            output_file
        ]
        await run_command(command)

        if os.path.exists(output_file):
            return output_file
        else:
            raise FileNotFoundError(f"Small video clip not created: {output_file}")
    except Exception as e:
        logger.error(f"Error in cult_small_video: {e}")
        raise


# Function to generate multiple screenshots from a video
async def generate_screen_shots(video_file, output_directory, is_watermarkable, watermark_file, min_duration, no_of_photos):
    try:
        metadata = extractMetadata(createParser(video_file))
        if not metadata or not metadata.has("duration"):
            raise ValueError("Unable to extract video duration from metadata.")

        duration = metadata.get('duration').seconds
        if duration <= min_duration:
            logger.info(f"Video duration is less than the minimum duration of {min_duration} seconds.")
            return None

        os.makedirs(output_directory, exist_ok=True)
        images = []
        ttl_step = duration // no_of_photos
        current_ttl = ttl_step

        for _ in range(no_of_photos):
            screenshot = await take_screen_shot(video_file, output_directory, current_ttl)
            current_ttl += ttl_step
            if is_watermarkable:
                watermarked_image = os.path.join(output_directory, f"{time.time()}_watermarked.jpg")
                screenshot = await place_water_mark(screenshot, watermarked_image, watermark_file)
            images.append(screenshot)

        return images
    except Exception as e:
        logger.error(f"Error in generate_screen_shots: {e}")
        raise


# Utility function to run subprocess commands
async def run_command(command):
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"Command {' '.join(command)} failed with error: {stderr.decode().strip()}")
    else:
        logger.debug(f"Command {' '.join(command)} executed successfully.")


# Main function to test the script
async def main():
    video_file = "path_to_your_video.mp4"
    output_directory = "./output_screenshots"
    watermark_file = "path_to_watermark.png"
    min_duration = 60  # Minimum duration of the video in seconds
    no_of_photos = 5  # Number of screenshots to generate

    try:
        screenshots = await generate_screen_shots(
            video_file, output_directory,
            is_watermarkable=True,
            watermark_file=watermark_file,
            min_duration=min_duration,
            no_of_photos=no_of_photos
        )
        logger.info(f"Generated screenshots: {screenshots}")
    except Exception as e:
        logger.error(f"Error in main: {e}")


if __name__ == "__main__":
    asyncio.run(main())
