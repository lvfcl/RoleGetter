import os
import shutil
import whisper
import subprocess
from datetime import timedelta

# my GPU is not powerful enough for large models, so I use CPU 
# you can chagne it

# === Step 1: Audio extract from the video ===
def extract_audio(video_path: str, audio_path: str):
    command = [
        r".\ffmpeg\bin\ffmpeg.exe",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path,
        "-y"
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"FFMPEG ended with an error:\n{result.stderr.decode()}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"[!] The file was not created: {audio_path}")

# ffmpeg works crookedly for me, and reinstalling Windows is a pain
# I think in the end this can be removed
def patch_ffmpeg():
    ffmpeg_path = r".\ffmpeg\bin\ffmpeg.exe"
    if not shutil.which("ffmpeg"):
        print("[INFO] ffmpeg is not found in PATH, add manually...")
        os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)
    else:
        print("[INFO] ffmpeg found:", shutil.which("ffmpeg"))

# === Step 2: Speech recognition with Whisper ===
def transcribe_audio(audio_path: str):
    patch_ffmpeg()
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"[!] The audio file was not found: {audio_path}")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["segments"]

# === Step 3: Formatting time for .ass format ===
def format_ass_time(seconds: float):
    t = timedelta(seconds=seconds)
    total_seconds = int(t.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    milliseconds = int((t.total_seconds() - total_seconds) * 100)
    return f"{hours:d}:{minutes:02d}:{secs:02d}.{milliseconds:02d}"

# === Step 4: Generation .ass file ===
def save_ass_file(segments, filepath):
    header = """[Script Info]
Title: Auto-generated Subtitles
ScriptType: v4.00+
Collisions: Normal
PlayResX: 1920
PlayResY: 1080
Timer: 100.0000
ScaledBorderAndShadow: yes
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,52,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1.5,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = ""
    for seg in segments:
        start = format_ass_time(seg['start'])
        end = format_ass_time(seg['end'])
        text = seg['text'].strip().replace("\n", " ")
        events += f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(events)

