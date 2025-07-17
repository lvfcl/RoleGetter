import os
import video_to_subtitles
import translate

VIDEO_PATH = ".\\video\\1_leak_version_Grand_Blue_Dreaming_Season_2_S02E07_480p_WEB_DL_AAC2.mp3"       # Замените на путь к вашему видео
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(BASE_DIR, "audio.wav")
ASS_OUTPUT = os.path.join(BASE_DIR, "subtitles.ass")
input_file = "subtitles.ass"
output_file = "subtitles_translated.ass"

if __name__ == "__main__":
    if not os.path.exists(VIDEO_PATH):
        print(f"[!] Video file was not found: {VIDEO_PATH}")
        exit(1)

    video_to_subtitles.extract_audio(VIDEO_PATH, AUDIO_PATH)
    print(f"[10%] Audio extraction...")
    segments = video_to_subtitles.transcribe_audio(AUDIO_PATH)
    print(f"[25%] Recognizing speech...")
    video_to_subtitles.save_ass_file(segments, ASS_OUTPUT)
    print(f"[50%] The creation of the original text has been completed")

    translate.translate_ass_with_deepl(input_file, output_file)
    print(f"[100%]The translation is completed")

