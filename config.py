import os
import logging
from dotenv import load_dotenv
from aiogram import Dispatcher

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
ENDPOINT = os.getenv("ENDPOINT")
RUNPOD_API = os.getenv("RUNPOD_API")

# Единый ключ для безопасного обмена данными между ботом и основным бэкендом.
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
          
dp = Dispatcher()