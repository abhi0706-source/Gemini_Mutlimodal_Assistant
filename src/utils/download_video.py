import logging
import os
import random
import time
from typing import Any, Dict, List, Optional

import requests
import yt_dlp
from bs4 import BeautifulSoup
from pytube import YouTube

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ContentDownloader:
    def __init__(self, download_path: str = "./downloads/"):
        self.download_path = download_path
        self.create_download_directory()

    def create_download_directory(self) -> None:
        """Create download directory if it doesn't exist."""
        os.makedirs(self.download_path, exist_ok=True)

    def _get_available_formats(self, url: str) -> List[Dict]:
        """Get list of available formats for a YouTube video."""
        ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": True}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [])
                # Filter for formats that have both video and audio
                combined_formats = [
                    f
                    for f in formats
                    if f.get("vcodec") != "none" and f.get("acodec") != "none"
                ]
                return combined_formats
        except Exception as e:
            logger.error(f"Error getting formats: {str(e)}")
            return []

    def download_youtube_content(
        self, url: str, download_audio: bool = False
    ) -> Optional[str]:
        """
        Download YouTube content with automatic format selection.
        """
        if download_audio:
            ydl_opts = {
                "outtmpl": os.path.join(self.download_path, "%(title)s.%(ext)s"),
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                    }
                ],
            }
        else:
            # Get available formats first
            formats = self._get_available_formats(url)
            if not formats:
                logger.error("No suitable formats found")
                return None

            # Configure options for video download
            ydl_opts = {
                "outtmpl": os.path.join(self.download_path, "%(title)s.%(ext)s"),
                "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b",  # Prefer MP4 format
                "merge_output_format": "mp4",
                "postprocessors": [
                    {
                        "key": "FFmpegVideoRemuxer",
                        "preferedformat": "mp4",
                    }
                ],
                "quiet": False,
                "no_warnings": False,
                "max_filesize": 2048 * 1024 * 1024,  # 2GB max
                "geo_bypass": True,
                "nocheckcertificate": True,
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-us,en;q=0.5",
                    "Sec-Fetch-Mode": "navigate",
                },
            }

        try:
            # First update yt-dlp
            os.system("yt-dlp -U")

            # Attempt download with yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info("Attempting download with yt-dlp...")
                ydl.download([url])
                return self.download_path

        except Exception as e:
            logger.warning(f"yt-dlp download failed: {str(e)}")
            logger.info("Attempting fallback to direct stream download...")
            return self._download_with_direct_stream(url)

    def _download_with_direct_stream(
        self, url: str, max_retries: int = 3
    ) -> Optional[str]:
        """Alternative download method using direct stream access."""
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    time.sleep(random.uniform(2, 5))

                yt = YouTube(url)
                # Sort streams by both resolution and bitrate
                streams = yt.streams.filter(progressive=True, file_extension="mp4")
                stream = streams.order_by("resolution").desc().first()

                if stream:
                    # Add random query parameter to avoid caching
                    timestamp = int(time.time())
                    stream.url = f"{stream.url}&_={timestamp}"

                    file_path = stream.download(
                        output_path=self.download_path,
                        filename_prefix=f"video_{timestamp}_",
                    )
                    logger.info(f"Successfully downloaded to: {file_path}")
                    return file_path
                else:
                    logger.error("No suitable stream found")
                    return None

            except Exception as e:
                logger.error(f"Download attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error("All download attempts failed")
                    return None


def downlaod_video_from_url(youtube_url="", download_path="./downloads/"):
    # Update yt-dlp first
    os.system("yt-dlp -U")

    downloader = ContentDownloader(download_path=download_path)



    # First, check available formats
    formats = downloader._get_available_formats(youtube_url)
    if formats:
        print("\nAvailable formats:")
        for f in formats:
            print(
                f"Format ID: {f.get('format_id')} - "
                f"Resolution: {f.get('resolution')} - "
                f"Filesize: {f.get('filesize_approx', 'unknown')} bytes"
            )

    # Download video with audio
    video_path = downloader.download_youtube_content(youtube_url)
    if video_path:
        print(f"\nVideo downloaded to: {video_path}")
    else:
        print("\nDownload failed")
