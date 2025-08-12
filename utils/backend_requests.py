import httpx
from dotenv import load_dotenv
import os 
import logging 

load_dotenv()
logging.basicConfig(level=logging.INFO)

AI_BACKEND_URL = os.getenv("AI_BACKEND_URL")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

async def send_audio_to_backend(wav_path: str):
    """Отправка аудио на бэк"""
    url = f"{AI_BACKEND_URL}/api/v1/internal/audio"
    headers = {"X-Internal-Api-Key": INTERNAL_API_KEY}

    async with httpx.AsyncClient() as client:
        with open(wav_path, "rb") as f:
            files = {"audio": (os.path.basename(wav_path), f, "audio/wav")}
            response = await client.post(url, files=files, headers=headers, timeout=30.0)
            response.raise_for_status()
    logging.info(f"Аудио {wav_path} успешно отправлено на бэк")


async def send_text_to_backend(text: str):
    """Отправка текста на бэк"""
    url = f"{AI_BACKEND_URL}/api/v1/internal/text"
    headers = {"X-Internal-Api-Key": INTERNAL_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"text": text}, headers=headers, timeout=30.0)
        response.raise_for_status()
    logging.info(f"Текст '{text}' успешно отправлен на бэк")