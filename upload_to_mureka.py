import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MUREKA_API_KEY")
FOLDER_PATH = os.getenv("MP3_FOLDER", "./converted_mp3")
API_BASE = "https://platform.mureka.ai/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


def create_upload():
    response = requests.post(f"{API_BASE}/uploads/create", headers=HEADERS, json={
        "purpose": "fine-tune"
    })
    response.raise_for_status()
    return response.json()["id"]


def upload_part(upload_id, part_number, file_path):
    with open(file_path, 'rb') as f:
        files = {
            "file": (os.path.basename(file_path), f),
            "part_number": (None, str(part_number))
        }
        response = requests.post(
            f"{API_BASE}/uploads/{upload_id}/parts",
            headers=HEADERS,
            files=files
        )
    response.raise_for_status()
    print(f"📤 Uploaded part {part_number}: {os.path.basename(file_path)}")


def complete_upload(upload_id):
    response = requests.post(f"{API_BASE}/uploads/{upload_id}/complete", headers=HEADERS)
    response.raise_for_status()
    print("🎉 Upload complete!")
    print(response.json())


def main():
    if not API_KEY:
        print("❌ Missing MUREKA_API_KEY in .env")
        return

    audio_files = sorted([
        os.path.join(FOLDER_PATH, f)
        for f in os.listdir(FOLDER_PATH)
        if f.lower().endswith(".mp3")
    ])

    if not (100 <= len(audio_files) <= 200):
        print(f"❌ You have {len(audio_files)} files. Mureka requires between 100 and 200.")
        return

    upload_id = create_upload()
    print(f"📦 Upload session created: {upload_id}")

    for i, file_path in enumerate(audio_files, start=1):
        upload_part(upload_id, i, file_path)

    complete_upload(upload_id)


if __name__ == "__main__":
    main()
