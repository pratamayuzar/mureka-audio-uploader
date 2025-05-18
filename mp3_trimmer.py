import os
import argparse
from pydub import AudioSegment

def trim_mp3_to_max_duration(source_folder, target_folder, max_duration):
    os.makedirs(target_folder, exist_ok=True)
    count = 0
    skipped = 0

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(".mp3"):
            mp3_path = os.path.join(source_folder, filename)
            output_path = os.path.join(target_folder, filename)

            if os.path.exists(output_path):
                print(f"⏭️ Skipping (already exists): {filename}")
                skipped += 1
                continue

            try:
                audio = AudioSegment.from_mp3(mp3_path)
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")
                continue

            if len(audio) > max_duration * 1000:
                print(f"⚠️ Truncating {filename} to {max_duration}s")
                audio = audio[:max_duration * 1000]

            audio.export(output_path, format="mp3", bitrate="192k")
            print(f"✅ Processed: {filename}")
            count += 1

    print(f"\n🎉 Total processed: {count}")
    print(f"⏭️ Skipped (already exists): {skipped}")

if __name__ == "__main__":
    # Sample usage:
    # python mp3_trimmer.py --source downloads --target converted_mp3 --max_duration 269

    parser = argparse.ArgumentParser(description="Trim and convert MP3 files")
    parser.add_argument("--source", type=str, required=True, help="Source folder containing MP3 files")
    parser.add_argument("--target", type=str, required=True, help="Target folder to save trimmed MP3 files")
    parser.add_argument("--max_duration", type=int, default=30, help="Maximum duration (in seconds)")

    args = parser.parse_args()

    trim_mp3_to_max_duration(args.source, args.target, args.max_duration)
    print("🎉 All MP3 files have been processed.")