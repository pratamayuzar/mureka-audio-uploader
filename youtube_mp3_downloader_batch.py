import argparse
import os
import subprocess
import requests
import time
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from isodate import parse_duration
from config import YOUTUBE_API_KEY


def search_youtube(query, max_total, max_per_page=10, page_token=None):
    url = (
        "https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&type=video&maxResults={max_per_page}&q={query}&key={YOUTUBE_API_KEY}"
    )
    if page_token:
        url += f"&pageToken={page_token}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_video_duration(video_id):
    url = (
        "https://www.googleapis.com/youtube/v3/videos?"
        f"part=contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
    )
    response = requests.get(url)
    items = response.json().get("items", [])
    if not items:
        return 0
    duration = items[0]["contentDetails"]["duration"]
    return parse_duration(duration).total_seconds()

def download_mp3(video_url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    result = subprocess.run([
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", f"{output_dir}/%(title)s.%(ext)s",
        video_url
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error downloading {video_url}:\n{result.stderr}")
    return result.stdout

def tag_mp3_files(directory, genre, album, title_artist_map):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            filepath = os.path.join(directory, filename)
            try:
                title = os.path.splitext(filename)[0]
                audio = MP3(filepath, ID3=EasyID3)
                audio['title'] = title
                audio['genre'] = genre
                audio['album'] = album
                if title in title_artist_map:
                    audio['artist'] = title_artist_map[title]
                audio.save()
                print(f"✅ Tagged '{filename}'")
            except Exception as e:
                print(f"⚠️ Failed to tag {filename}: {e}")

def main():
    # Sample usage:
    # python youtube_mp3_downloader_batch.py --query "koplo" --max 100 --genre "Koplo" --max_duration 600
    
    parser = argparse.ArgumentParser(description="Batch YouTube MP3 downloader with metadata tagging")
    parser.add_argument('--query', type=str, required=True, help="Search keyword (e.g. 'koplo')")
    parser.add_argument('--max', type=int, default=100, help="Total songs to download")
    parser.add_argument('--genre', type=str, default="Unknown", help="MP3 Genre")
    parser.add_argument('--max_duration', type=int, default=600, help="Max video duration (in seconds)")
    args = parser.parse_args()

    output_dir = "downloads"
    downloaded = 0
    page_token = None
    title_artist_map = {}

    while downloaded < args.max:
        response = search_youtube(args.query, args.max, max_per_page=10, page_token=page_token)
        items = response.get("items", [])
        page_token = response.get("nextPageToken")

        if not items:
            print("No more videos found.")
            break

        for item in items:
            if downloaded >= args.max:
                break

            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            artist = item["snippet"]["channelTitle"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            safe_filename = f"{title}.mp3"

            # Skip if already exists
            if os.path.exists(os.path.join(output_dir, safe_filename)):
                print(f"⏩ Skipping already downloaded: {title}")
                continue

            # Check duration
            try:
                duration = get_video_duration(video_id)
            except Exception as e:
                print(f"⚠️ Failed to get duration for {title}: {e}")
                continue

            if duration > args.max_duration:
                print(f"⏩ Skipping '{title}' (>{args.max_duration}s)")
                continue

            print(f"🎵 Downloading: {title} ({int(duration)}s)")
            try:
                download_mp3(video_url, output_dir)
                title_artist_map[title] = artist
                downloaded += 1
                time.sleep(1)  # Small pause to avoid hammering the API
            except Exception as e:
                print(f"❌ Failed to download {title}: {e}")

        if not page_token:
            break

    print("🏷️ Tagging MP3 files...")
    tag_mp3_files(output_dir, args.genre, args.query, title_artist_map)
    print(f"✅ Finished. Total downloaded: {downloaded}")

if __name__ == "__main__":
    main()
