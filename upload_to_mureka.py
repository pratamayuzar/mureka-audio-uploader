import argparse
import os
import requests
import shutil
from pydub.utils import mediainfo
from config import API_KEY, API_BASE, TARGET_FOLDER, SUCCESS_FOLDER, FAIL_FOLDER, MIN_DURATION, MAX_DURATION


HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

os.makedirs(SUCCESS_FOLDER, exist_ok=True)

def create_upload():
    response = requests.post(f"{API_BASE}/v1/uploads/create", headers=HEADERS, json={
        "upload_name": "lagoe-01",
        "purpose": "fine-tune"
    })
    response.raise_for_status()
    return response.json()["id"]

# old version
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


def upload_file(upload_id, file_path):
    print(f"📤 Uploading: {os.path.basename(file_path)}")
    with open(file_path, 'rb') as f:
        files = {
            "file": (os.path.basename(file_path), f),
            "upload_id": (None, upload_id)
        }
        try:
            response = requests.post(
                f"{API_BASE}/v1/uploads/add",
                headers=HEADERS,
                files=files
            )
            response.raise_for_status()
            print(f"✅ Uploaded: {os.path.basename(file_path)}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to upload: {os.path.basename(file_path)}")
            print(f"📄 Response: {response.text}")
            return False

def is_valid_duration(file_path):
    info = mediainfo(file_path)
    duration = float(info['duration'])
    
    if MIN_DURATION <= duration <= (MAX_DURATION + 1):
        return True
    else:
        print(f"❌ Invalid duration: {duration} seconds (allowed: {MIN_DURATION}–{MAX_DURATION + 1})")
        return False


def complete_upload(upload_id):
    try:
        response = requests.post(
            f"{API_BASE}/v1/uploads/complete",
            headers=HEADERS,
            json={"upload_id": upload_id}
        )
        response.raise_for_status()
        print("🎉 Upload complete!")
        print(response.json())
    except requests.exceptions.HTTPError as e:
        print("❌ Failed to complete upload.")
        print(f"Status Code: {e.response.status_code}")
        print("Response Body:", e.response.text)


def main(upload_id=None, limit=None, complete=False):
    if not API_KEY:
        print("❌ Missing MUREKA_API_KEY in .env")
        return

    audio_files = sorted([
        os.path.join(TARGET_FOLDER, f)
        for f in os.listdir(TARGET_FOLDER)
        if f.lower().endswith(".mp3")
    ])

    if limit:
        audio_files = audio_files[:limit]
        print(f"⚙️ Limiting to first {limit} files")

    if not upload_id:
        upload_id = create_upload()
        print(f"📦 New upload session created: {upload_id}")
    else:
        print(f"📦 Reusing existing upload_id: {upload_id}")

    if not complete:
        # Upload files if `--complete` flag is not set
        for i, file_path in enumerate(audio_files, start=1):
            if not is_valid_duration(file_path):
                print(f"⏩ Skipping {os.path.basename(file_path)} — duration not in range.")
                continue

            success = upload_file(upload_id, file_path)
            filename = os.path.basename(file_path)

            if success:
                # Move to success folder
                dest_path = os.path.join(SUCCESS_FOLDER, filename)
                shutil.move(file_path, dest_path)
                print(f"✅ Moved to success: {filename}")
            else:
                # Move to fail folder
                dest_path = os.path.join(FAIL_FOLDER, filename)
                shutil.move(file_path, dest_path)
                print(f"❌ Moved to fail: {filename}")

    if complete:
        complete_upload(upload_id)
    else:
        print(f"ℹ️ Upload ID `{upload_id}` ready — call `complete_upload(upload_id)` when done.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--upload-id", help="Reuse an existing upload_id")
    parser.add_argument("--limit", type=int, help="Limit number of files to upload")
    parser.add_argument("--complete", action="store_true", help="Complete the upload after sending files")
    args = parser.parse_args()

    main(upload_id=args.upload_id, limit=args.limit, complete=args.complete)
