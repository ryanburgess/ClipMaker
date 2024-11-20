import os
import sys
import ffmpeg
from whisper import load_model
from pydub import AudioSegment, silence

def process_media(file_path, output_dir, is_audio=False):
    os.makedirs(output_dir, exist_ok=True)

    # Load Whisper model for transcription
    model = load_model("base")  # Adjust model size as needed

    # Extract audio for silence detection
    audio_path = os.path.join(output_dir, "temp_audio.wav")
    if is_audio:
        # If it's an audio file, just copy it for processing
        audio = AudioSegment.from_file(file_path)
    else:
        # If it's a video file, extract audio
        ffmpeg.input(file_path).output(audio_path, ac=1, ar=16000).run(overwrite_output=True)
        audio = AudioSegment.from_wav(audio_path)

    # Detect non-silent segments
    silence_threshold = -40  # Adjust based on your audio setup
    silence_chunks = silence.detect_nonsilent(audio, min_silence_len=500, silence_thresh=silence_threshold)

    # Process each non-silent segment
    for idx, (start_ms, end_ms) in enumerate(silence_chunks):
        start_sec = start_ms / 1000
        end_sec = end_ms / 1000

        # Generate output file name
        file_extension = "mp3" if is_audio else "mp4"
        clip_output_path = os.path.join(output_dir, f"clip_{idx}.{file_extension}")

        if is_audio:
            # Extract audio segment
            segment = audio[start_ms:end_ms]
            segment.export(clip_output_path, format="mp3")
        else:
            # Extract video and audio for the segment
            ffmpeg.input(file_path, ss=start_sec, to=end_sec).output(clip_output_path).run(overwrite_output=True)

        # Transcribe the segment for naming
        result = model.transcribe(clip_output_path)
        transcription = result["text"].strip()
        sanitized_name = transcription.replace(" ", "_").replace("/", "-")
        renamed_clip_path = os.path.join(output_dir, f"{sanitized_name} - take {idx+1}.{file_extension}")

        # Rename the clip file
        os.rename(clip_output_path, renamed_clip_path)

    # Clean up temp audio file if processing video
    if not is_audio and os.path.exists(audio_path):
        os.remove(audio_path)

    print(f"Processed {'audio' if is_audio else 'video'} clips saved in: {output_dir}")

def process_folder(folder_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    media_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(('.mp4', '.mov', '.mkv', '.wav', '.mp3'))
    ]

    if not media_files:
        print(f"No media files found in {folder_path}.")
        return

    for media_file in media_files:
        file_path = os.path.join(folder_path, media_file)
        file_output_dir = os.path.join(output_dir, os.path.splitext(media_file)[0])
        is_audio = media_file.lower().endswith(('.wav', '.mp3'))
        process_media(file_path, file_output_dir, is_audio)

def main():
    if len(sys.argv) < 2:
        print("Usage: python ClipMaker.py <media_file_or_folder>")
        return

    input_path = sys.argv[1]
    output_dir = "processed_clips"

    if os.path.isdir(input_path):
        print(f"Processing all media files in folder: {input_path}")
        process_folder(input_path, output_dir)
    elif os.path.isfile(input_path):
        is_audio = input_path.lower().endswith(('.wav', '.mp3'))
        print(f"Processing single {'audio' if is_audio else 'video'} file: {input_path}")
        process_media(input_path, output_dir, is_audio)
    else:
        print(f"Invalid path: {input_path}")

if __name__ == "__main__":
    main()