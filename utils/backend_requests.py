import httpx
from dotenv import load_dotenv
import os 
import logging 

load_dotenv()
logging.basicConfig(level=logging.INFO)

AI_BACKEND_URL = os.getenv("AI_BACKEND_URL")

async def send_audio_to_backend(wav_path: str, chat_id: int):
    """Отправка аудио на бэк"""
    url = f"{AI_BACKEND_URL}/api/v1/internal/audio"
    headers = {"X-Internal-Api-Key": 'key'}

    async with httpx.AsyncClient() as client:
        with open(wav_path, "rb") as f:
            files = {"audio": (os.path.basename(wav_path), f, "audio/wav")}
            data = {"chat_id": str(chat_id)}
            response = await client.post(url, files=files, data=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            result = response.json()

    logging.info(f"[chat_id={chat_id}] Аудио {wav_path} успешно обработано на бэке")
    return result.get("text", "")


async def send_text_to_backend(text: str, chat_id: int):
    """Отправка текста на бэк"""
    url = f"{AI_BACKEND_URL}/api/v1/internal/text"
    headers = {"X-Internal-Api-Key": 'key'}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, json={"text": text, "chat_id": chat_id}, headers=headers, timeout=30.0
        )
        response.raise_for_status()
        result = response.json()

    logging.info(f"[chat_id={chat_id}] Текст '{text}' успешно обработан на бэке")
    return result.get("text", text)