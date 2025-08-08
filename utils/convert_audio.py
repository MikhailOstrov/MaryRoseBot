import os
from pydub import AudioSegment
import logging

AudioSegment.converter = r"D:/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffprobe = r"D:/ffmpeg/bin/ffprobe.exe"

logging.basicConfig(level=logging.INFO)

def convert_audio_to_wav(original_ogg_path: str) -> str:
        
        audio = AudioSegment.from_file(original_ogg_path)

        base_filename = os.path.splitext(os.path.basename(original_ogg_path))[0]

        wav_path = os.path.join("converted", f"{base_filename}.wav")
        audio.export(wav_path, format="wav")
        logging.info(f"Файл конвертирован в WAV: {wav_path}")

        return wav_path