# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Update the package list and install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg aria2 git wget pv jq python3-dev mediainfo && \
    rm -rf /var/lib/apt/lists/*

# Verify FFmpeg installation and check the version
RUN ffmpeg -version

# Install the latest version of yt-dlp directly from GitHub
RUN wget -q https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --force-reinstall brotli motor

# Verify yt-dlp and motor installation
RUN yt-dlp --version && python3 -m pip check

# Copy the application code
COPY . .

# Add a non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Set the default command to run the bot
CMD ["python3", "bot.py"]

