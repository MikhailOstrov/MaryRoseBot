import os
import logging
from dotenv import load_dotenv
from aiogram import Dispatcher
from openai import AsyncOpenAI

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN") # Токен бота
RUNPOD_API = os.getenv("RUNPOD_API") # От RunPod (API)
AI_BACKEND_URL = os.getenv("AI_BACKEND_URL") # От RunPod (ID)
BACKEND_URL = os.getenv("BACKEND_URL") # От бэка с БД
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY") # Ключ от бэка с БД

# Клиент OpenAI
CLIENT_AS = AsyncOpenAI(
    api_key=os.getenv("PROXY_API"),
    base_url=os.getenv("BASE_OPENAI_URL"),
)

# Под конвертацию аудио
ffmpeg_path = os.getenv("FFMPEG_PATH")
ffprobe_path = os.getenv("FFPROBE_PATH")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
          
dp = Dispatcher()