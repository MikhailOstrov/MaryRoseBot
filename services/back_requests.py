from dotenv import load_dotenv
import logging
import requests
import base64
from config import ENDPOINT, RUNPOD_API

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def send_audio_to_backend(audio_bytes: bytes, chat_id: int) -> str:
    """
    Отправляет байты аудио на serverless-бэкенд для транскрибации.
    """
    try:
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        
        payload = {
            "input": {
                "chat_id": chat_id,
                "audio_b64": audio_b64
            }
        }
        
        headers = {"Authorization": f"Bearer {RUNPOD_API}"}
        
        r = requests.post(ENDPOINT, json=payload, headers=headers)
        r.raise_for_status()
        
        response_data = r.json()
        
        text = response_data.get('output', {}).get('text')
        return text
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при отправке запроса на бэкэнд: {e}")