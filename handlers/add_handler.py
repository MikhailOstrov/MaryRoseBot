from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from aiogram import Bot, F
import os

from states.kb_states import AddKnowledge
from services.kb_requests import save_info_in_kb
from services.back_requests import send_audio_to_backend
from utils.convert_audio import convert_audio_to_wav
from config import logger

router = Router()

# /add
@router.message(lambda message: message.text == "Добавить знание")
async def start_add(message: Message, state: FSMContext):
    await message.answer("📝 Введите текст, который нужно сохранить в базу знаний:")
    await state.set_state(AddKnowledge.waiting_for_text)

@router.message(AddKnowledge.waiting_for_text, F.text)
async def process_add_text(message: Message, state: FSMContext):
    await save_info_in_kb(message.text, message.chat.id)
    await message.answer("Текст сохранён в базу знаний.")
    await state.clear()

@router.message(AddKnowledge.waiting_for_text, F.voice | F.audio)
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

        await save_info_in_kb(response_audio, chat_id)
        await message.answer("Аудио расшифровано и сохранено в базу знаний.")
        await state.clear()

    except Exception as e:
        logger.error(f"Ошибка при обработке аудио: {e}")

    finally:
        if os.path.exists(temp_ogg_path):
            os.remove(temp_ogg_path)

