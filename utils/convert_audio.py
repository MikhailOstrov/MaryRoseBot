import os
from pydub import AudioSegment

from config import ffmpeg_path, ffprobe_path, logger

if ffmpeg_path:
        AudioSegment.converter = ffmpeg_path
if ffprobe_path:
        AudioSegment.ffprobe = ffprobe_path

def convert_audio_to_wav(original_ogg_path: str) -> str:
        
        os.makedirs("converted", exist_ok=True)

        audio = AudioSegment.from_file(original_ogg_path)
        base_filename = os.path.splitext(os.path.basename(original_ogg_path))[0]

        wav_path = os.path.join("converted", f"{base_filename}.wav")
        audio.export(wav_path, format="wav")
        logger.info(f"Файл конвертирован в WAV: {wav_path}")

        return wav_path