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
git clone https://github.com/your-username/mureka-audio-uploader.git
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
├── convert_wav_to_mp3.py      # Convert script
├── upload_to_mureka.py        # Upload script
├── requirements.txt
├── README.md
├── .env
├── wav_files/                 # Place original WAV files here
└── converted_mp3/             # MP3 output goes here
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

Then run:

```bash
python upload_to_mureka.py
```

The script will:
- Create a new upload session
- Upload all MP3 files as parts
- Complete the upload

---

## 🔐 Tips

- Mureka currently only supports 100–200 files per upload session.
- Use high-quality `.wav` files for better fine-tune results.

---

## 🛠 Future Improvements

- Retry failed uploads
- CLI flags for custom folders or environment overrides
- Progress bar for uploads

---

## 📄 License

MIT – feel free to fork and customize.

Made with ❤️ for Mureka.ai integrations.