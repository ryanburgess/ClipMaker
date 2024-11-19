import os
import sys
import ffmpeg
from whisper import load_model
from pydub import AudioSegment, silence

def process_video(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Load Whisper model for transcription
    model = load_model("base")  # Adjust model size as needed

    # Extract audio for silence detection
    audio_path = os.path.join(output_dir, "temp_audio.wav")
    ffmpeg.input(video_path).output(audio_path, ac=1, ar=16000).run(overwrite_output=True)
    audio = AudioSegment.from_wav(audio_path)

    # Detect non-silent segments
    silence_threshold = -40  # Adjust based on your audio setup
    silence_chunks = silence.detect_nonsilent(audio, min_silence_len=500, silence_thresh=silence_threshold)

    # Process each non-silent segment
    for idx, (start_ms, end_ms) in enumerate(silence_chunks):
        start_sec = start_ms / 1000
        end_sec = end_ms / 1000

        # Generate output file name
        clip_output_path = os.path.join(output_dir, f"clip_{idx}.mp4")

        # Extract video and audio for the segment
        ffmpeg.input(video_path, ss=start_sec, to=end_sec).output(clip_output_path).run(overwrite_output=True)

        # Transcribe the segment for naming
        result = model.transcribe(clip_output_path)
        transcription = result["text"].strip()
        sanitized_name = transcription.replace(" ", "_").replace("/", "-")
        renamed_clip_path = os.path.join(output_dir, f"{sanitized_name} - take {idx+1}.mp4")

        # Rename the clip file
        os.rename(clip_output_path, renamed_clip_path)

    # Clean up temp audio file
    os.remove(audio_path)
    print(f"Processed video clips saved in: {output_dir}")

def process_folder(folder_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mov', '.mkv'))]

    if not video_files:
        print(f"No video files found in {folder_path}.")
        return

    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        video_output_dir = os.path.join(output_dir, os.path.splitext(video_file)[0])
        process_video(video_path, video_output_dir)

def main():
    if len(sys.argv) < 2:
        print("Usage: python ClipMaker.py <video_file_or_folder>")
        return

    input_path = sys.argv[1]
    output_dir = "processed_clips"

    if os.path.isdir(input_path):
        print(f"Processing all video files in folder: {input_path}")
        process_folder(input_path, output_dir)
    elif os.path.isfile(input_path):
        print(f"Processing single video file: {input_path}")
        process_video(input_path, output_dir)
    else:
        print(f"Invalid path: {input_path}")

if __name__ == "__main__":
    main()