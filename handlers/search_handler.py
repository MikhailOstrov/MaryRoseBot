from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F, Bot
import os

from states.kb_states import SearchKnowledge
from services.kb_requests import get_info_from_kb
from utils.llm_handler import response_for_searh
from services.back_requests import send_audio_to_backend
from utils.convert_audio import convert_audio_to_wav
from config import logger

router = Router()

# /search
@router.message(lambda message: message.text == "Найти знание")
async def start_search(message: Message, state: FSMContext):
    await message.answer("🔎 Введите запрос для поиска в базе знаний:")
    await state.set_state(SearchKnowledge.waiting_for_query)

@router.message(SearchKnowledge.waiting_for_query, F.text)
async def process_search(message: Message, state: FSMContext):
    search_text = await response_for_searh(message.text)
    result = await get_info_from_kb(search_text, message.chat.id)
    await message.answer(result)
    await state.clear()

@router.message(SearchKnowledge.waiting_for_query, F.voice | F.audio)
async def process_add_audio(message: Message, state: FSMContext, bot: Bot):
    chat_id = message.chat.id
    file_id = message.voice.file_id if message.voice else message.audio.file_id

    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Создаем полный путь к временному OGG-файлу.
    temp_ogg_path = os.path.join(temp_dir, f"{file_id}.ogg")

    try:
        # 1. Получаем информацию о файле и скачиваем его
        file_info = await bot.get_file(file_id)
        
        # Скачиваем файл во временное место на диске
        await bot.download_file(file_info.file_path, destination=temp_ogg_path)
        logger.info(f"Аудиофайл скачан в {temp_ogg_path}")
        
        wav_path = convert_audio_to_wav(temp_ogg_path)
        logger.info(f"Конвертация завершена. WAV-файл: {wav_path}")

        response_audio = await send_audio_to_backend(wav_path, chat_id)
        
        search_text = await response_for_searh(response_audio)
        result = await get_info_from_kb(search_text, message.chat.id)
        await message.answer(result)
        await state.clear()
        
    except Exception as e:
        logger.error(f"Ошибка при обработке аудио: {e}")
        await message.reply("Произошла ошибка при обработке аудиофайла. Попробуйте еще раз.")

    finally:
        if os.path.exists(temp_ogg_path):
            os.remove(temp_ogg_path)