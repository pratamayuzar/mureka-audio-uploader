import os
from pydub import AudioSegment
from config import SOURCE_FOLDER, TARGET_FOLDER, MAX_DURATION

def convert_wav_to_mp3():
    os.makedirs(TARGET_FOLDER, exist_ok=True)
    count = 0
    for filename in os.listdir(SOURCE_FOLDER):
        if filename.lower().endswith(".wav"):
            wav_path = os.path.join(SOURCE_FOLDER, filename)
            mp3_path = os.path.join(TARGET_FOLDER, os.path.splitext(filename)[0] + ".mp3")

            audio = AudioSegment.from_wav(wav_path)
            # Truncate if longer than MAX_DURATION_SECONDS
            if len(audio) > MAX_DURATION * 1000:
                print(f"⚠️ Truncating {filename} to {MAX_DURATION}s")
                audio = audio[:MAX_DURATION * 1000]

            audio.export(mp3_path, format="mp3", bitrate="192k")

            print(f"✅ Converted: {filename} → {os.path.basename(mp3_path)}")
            count += 1
    
    print(f"\n🎉 Total files converted: {count}")

if __name__ == "__main__":
    convert_wav_to_mp3()
    print("🎉 All WAV files have been converted to MP3.")