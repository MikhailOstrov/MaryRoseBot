import logging
from aiogram import Dispatcher
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
ENDPOINT = os.getenv("ENDPOINT")
RUNPOD_API = os.getenv("RUNPOD_API")
          
dp = Dispatcher()