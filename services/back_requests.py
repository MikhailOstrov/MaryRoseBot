from dotenv import load_dotenv
import logging
import requests
import base64
import os

from config import ENDPOINT, RUNPOD_API

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def send_audio_to_backend(wav_path: str, chat_id: int) -> str:
    try:
        with open(wav_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        
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
    
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)
            logging.info(f"Файл {wav_path} успешно удален.")