# 🎧 Mureka Fine-Tune Audio Uploader

A Python-based tool to convert `.wav` audio files to `.mp3` and upload them to [Mureka](https://platform.mureka.ai) for fine-tuning.

---

## ✅ Features

- Convert `.wav` files to `.mp3` format
- Upload 100–200 audio files to Mureka
- Split into two simple scripts for flexibility
- Secure config with `.env` file

---

## 🧰 Requirements

- Python 3.7+
- FFmpeg (for audio conversion)
- Internet connection
- Mureka API key

---

## ⚙️ Installation & Setup

### 1. Install FFmpeg

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update && sudo apt install ffmpeg
```

#### Windows
- Download from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Extract it
- Add the `bin/` folder to your system PATH

---

### 2. Clone & Setup Python Environment

```bash
git clone https://github.com/pratamayuzar/mureka-audio-uploader.git
cd mureka-audio-uploader

# Create virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Create `.env` File

Create a `.env` file in the root directory:

```env
MUREKA_API_KEY=your_mureka_api_key
MP3_FOLDER=./converted_mp3
```

Replace `your_mureka_api_key` with your actual API key from Mureka.

---

## 📂 Folder Structure

```
project-folder/
├── convert_wav_to_mp3.py      # Convert WAV → MP3
├── upload_to_mureka.py        # Upload trimmed MP3s to Mureka
├── download_youtube.py        # NEW: Download MP3s from YouTube by keyword
├── mp3_trimmer.py             # NEW: Trim MP3s to fixed length
├── requirements.txt
├── README.md
├── .env
├── wav_files/
├── converted_mp3/
├── downloads/                 # NEW: Raw MP3s from YouTube
└── trimmed/                   # NEW: Trimmed MP3s ready for upload
```

---

## 🚀 Usage

### 1. Convert `.wav` → `.mp3`

Make sure your `.wav` files are in the `wav_files/` folder:

```bash
python convert_wav_to_mp3.py
```

This creates `.mp3` files in the `converted_mp3/` folder.

---

### 2. Upload to Mureka

Ensure you have between **100 and 200** `.mp3` files in the `converted_mp3/` folder.

You can run the script with the following options:

### Arguments

- `--upload-id UPLOAD_ID`:
  Reuse an existing upload session. If not provided, a new upload session will be created.
  
- `--limit LIMIT`:
  Limit the number of files to upload. For example, `--limit 5` will upload the first 5 files.

- `--complete`:
  Complete the upload after sending the files. If not provided, the upload session will remain open, and you can complete it manually later.

### Examples

1. **Upload first 3 files** (without completing):
   ```bash
   python upload_to_mureka.py --limit 3
   ```

2. **Upload all files and complete the session**:
   ```bash
   python upload_to_mureka.py --complete
   ```

3. **Reuse an existing upload session and complete**:
   ```bash
   python upload_to_mureka.py --upload-id 1436211 --complete
   ```

---

### 3. Download from YouTube

This script helps you search and download up to 100 songs from YouTube based on a keyword or genre.

#### Usage

```bash
python download_youtube.py --query "koplo remix" --limit 100 --output ./downloads
```

#### Arguments

* `--query` (required): Search term (e.g., `koplo remix`)
* `--limit`: Max number of songs to download (default: 10)
* `--output`: Target folder for downloaded MP3s (default: `downloads`)

The script also retrieves basic metadata (title, artist, album) if available.

---

### 4. Trim MP3 Files

This trims `.mp3` files to a maximum duration (e.g., 30 seconds) and saves them to another folder. Useful for preparing fine-tuning datasets.

#### Usage

```bash
python mp3_trimmer.py --source ./downloads --target ./trimmed --max_duration 30
```

#### Arguments

* `--source` (required): Folder with original MP3s
* `--target` (required): Destination folder for trimmed MP3s
* `--max_duration`: Maximum length in seconds (default: 30)

✅ Files already present in the target folder will be skipped automatically.

---

## 🔐 Tips

- Mureka currently only supports 100–200 files per upload session.

---

## 🛠 Future Improvements

- Retry failed uploads
- CLI flags for custom folders or environment overrides
- Progress bar for uploads

---

## 📄 License

MIT – feel free to fork and customize.

Made with ❤️ for Mureka.ai integrations.