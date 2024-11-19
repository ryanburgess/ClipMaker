# ClipMaker

**ClipMaker** is a Python script designed to streamline video editing by automatically detecting speech segments, trimming dead space, splitting videos into clips, and naming them based on transcribed text. It's perfect for creators, editors, and anyone working with repetitive takes or content-heavy video files.

---

## Features

- Removes silent segments from videos.
- Splits videos into individual clips based on speech.
- Automatically names clips using speech transcription.
- Processes single files or entire folders of video files.
- Works with common video formats like `.mp4`, `.mov`, and `.mkv`.

---

## Requirements

- Python 3.7 or later
- FFmpeg installed and added to your system's PATH. [Download FFmpeg](https://ffmpeg.org/download.html)
- Required Python libraries:
  ```bash
  pip install ffmpeg-python pydub openai-whisper