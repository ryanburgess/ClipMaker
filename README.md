
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
- **FFmpeg** installed and added to your PATH. You can easily install FFmpeg using Homebrew:
  ```bash
  brew install ffmpeg
  ```
  Verify the installation:
  ```bash
  ffmpeg -version
  ```
- Required Python libraries:
  ```bash
  pip install ffmpeg-python pydub openai-whisper
  ```

---

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/clipmaker.git
   cd clipmaker
   ```

2. **Install Dependencies**:
   Run the following command to install all required libraries:
   ```bash
   pip install ffmpeg-python pydub openai-whisper
   ```

3. **Make ClipMaker Executable Globally**:
   - Add the script to a directory in your PATH, such as `/usr/local/bin`.
   - Rename the script to `ClipMaker` (no file extension) for simplicity:
     ```bash
     mv clipmaker.py /usr/local/bin/ClipMaker
     chmod +x /usr/local/bin/ClipMaker
     ```

   - Alternatively, create a bash alias in your `~/.bashrc` or `~/.zshrc`:
     ```bash
     alias ClipMaker="python /path/to/clipmaker.py"
     ```

4. **Verify FFmpeg Installation**:
   Ensure FFmpeg is installed and accessible from the command line:
   ```bash
   ffmpeg -version
   ```

---

## Usage

### Process a Single Video File
To process a single video file, run:
```bash
ClipMaker /path/to/your/video.mp4
```

### Process All Videos in a Folder
To process all videos in a folder, run:
```bash
ClipMaker /path/to/your/folder
```

### Process Videos in the Current Directory
To process videos in the current directory:
```bash
ClipMaker .
```

### Output
- Processed clips are saved in a `processed_clips` folder.
- Each clip is named based on the transcribed text (e.g., `The_best_part_of_leadership - take 1.mp4`).

---

## Output Quality and File Preservation

- **Lossless Quality**:  
  ClipMaker preserves the original quality of your video and audio files. No re-encoding is applied by default, ensuring there is no loss in resolution, bitrate, or frame rate. The audio also remains untouched, retaining its original fidelity.

- **File Format**:  
  The output files will inherit the same format as the input files (e.g., `.mp4`, `.mov`, `.mkv`), ensuring compatibility and consistency.

- **Original Files**:  
  The script does not modify your original video files. Instead, it creates new files for each processed clip and saves them in a separate folder (`processed_clips`), leaving the original files intact.

- **Fast Processing**:  
  Since no re-encoding is performed, ClipMaker processes videos quickly, trimming and splitting files with minimal overhead.

---

## Advanced Options for Re-Encoding (Optional)

By default, ClipMaker does not re-encode video or audio streams. However, if you need to re-encode (e.g., to standardize file formats or reduce file sizes), you can modify the FFmpeg command in the script.

For example:
```python
ffmpeg.input(video_path, ss=start_sec, to=end_sec).output(clip_output_path, vcodec="libx264", acodec="aac").run(overwrite_output=True)
```
- `vcodec="libx264"`: Re-encodes the video to H.264 (widely supported codec).
- `acodec="aac"`: Re-encodes audio to AAC (common audio format).

> **Note**: Re-encoding may result in quality loss and longer processing times. Use this only if required.

---

## Contributing

If you’d like to contribute, feel free to fork the repository and submit a pull request. Suggestions and improvements are welcome!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Known Issues

- **Speech-to-Text Accuracy**: Ensure clear audio for the best transcription results.
- **Silent Detection Tweaks**: Adjust the silence threshold and minimum silence length in the script for better segmentation.

---
