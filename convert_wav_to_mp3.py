import os
from pydub import AudioSegment

SOURCE_FOLDER = "./wav_files"
TARGET_FOLDER = "./converted_mp3"

def convert_wav_to_mp3():
    os.makedirs(TARGET_FOLDER, exist_ok=True)
    for filename in os.listdir(SOURCE_FOLDER):
        if filename.lower().endswith(".wav"):
            wav_path = os.path.join(SOURCE_FOLDER, filename)
            mp3_path = os.path.join(TARGET_FOLDER, os.path.splitext(filename)[0] + ".mp3")

            audio = AudioSegment.from_wav(wav_path)
            audio.export(mp3_path, format="mp3", bitrate="192k")

            print(f"✅ Converted: {filename} → {os.path.basename(mp3_path)}")

if __name__ == "__main__":
    convert_wav_to_mp3()
