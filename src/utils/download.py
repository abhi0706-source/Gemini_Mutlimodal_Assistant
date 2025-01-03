import os
import traceback

import requests
import yt_dlp
from bs4 import BeautifulSoup
from download_video import downlaod_video_from_url
from pytube import YouTube


def download_youtube_video(url, download_path="../data/"):
    try:
        yt = YouTube(url)

        # Get the best stream (highest resolution video)
        video_stream = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )

        # If the stream exists, download it
        if video_stream:
            video_stream.download(output_path=download_path)
            print(f"Video downloaded successfully to {download_path}")
        else:
            print("No suitable video stream found")
    except Exception as e:
        print(f"Error in downloading YouTube video: {e}")


def download_audio(url, download_path="../data/"):
    """
    Download audio from YouTube and convert to MP3 format.

    Args:
        url: YouTube video URL
        download_path: Path where the MP3 file will be saved
    """
    ydl_opts = {
        "outtmpl": f"{download_path}%(title)s.%(ext)s",
        "format": "bestaudio/best",
        "geo-bypass": True,
        "noplaylist": True,
        "force-ipv4": True,
        # Add postprocessors for MP3 conversion
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Audio downloaded and converted to MP3 successfully at {download_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to download PDF, DOC, or other files
def download_file(url, download_path="../data/"):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        filename = os.path.join(download_path, url.split("/")[-1])

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"File downloaded successfully to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to download text or webpage content
def download_text_or_webpage(url, download_path="../data/", is_text=False):
    try:
        response = requests.get(url)
        response.raise_for_status()

        if is_text:
            filename = os.path.join(download_path, url.split("/")[-1] + ".txt")
            with open(filename, "w") as file:
                file.write(response.text)
            print(f"Text file downloaded successfully to {filename}")
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            filename = os.path.join(download_path, url.split("/")[-1] + ".html")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(soup.prettify())
            print(f"Webpage downloaded successfully to {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Example Usage:
    # url_video = "https://www.youtube.com/watch?v=dIYmzf21d1g"
    # downlaod_video_from_url(
    #     youtube_url=url_video, download_path="../data/"
    # )  # Download video
    url_audio = "https://www.youtube.com/watch?v=8OHYynw7Yh4"
    download_audio(url_audio)  # Download audio

    # url_pdf = "https://example.com/somefile.pdf"
    # download_file(url_pdf)  # Download PDF, DOC, or any other file

    # url_text = "https://example.com/sometextfile"
    # download_text_or_webpage(url_text, is_text=True)  # Download text

    # url_webpage = "https://en.wikipedia.org/wiki/Microsoft"
    # download_text_or_webpage(url_webpage)  # Download webpage content


if __name__ == "__main__":
    main()
