from aiogram.types import Message
from aiogram import Bot, F
from config import logger
import os
from utils.convert_audio import convert_audio_to_wav
from services.back_requests import send_audio_to_backend
from aiogram import Router

router = Router()

# Хендлер на аудио и голосовые сообщения
@router.message(F.voice | F.audio)
async def audio_message_handler(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    file_id = message.voice.file_id if message.voice else message.audio.file_id
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    if not os.path.exists("converted"):
        os.makedirs("converted")

    try:

        file_info = await bot.get_file(file_id)
        original_ogg_path = os.path.join("downloads", file_info.file_path.split('/')[-1])
        await bot.download_file(file_info.file_path, destination=original_ogg_path)
        logger.info(f"Оригинальный файл сохранен: {original_ogg_path}")

        wav_path = convert_audio_to_wav(original_ogg_path)
        
        try:
            response_audio = await send_audio_to_backend(wav_path, chat_id)
            await bot.send_message(chat_id, f"{response_audio}")
        except Exception as e:
            logger.error(f"Ошибка отправки аудио на бэк: {e}")

    except Exception as e:
        logger.error(f"Ошибка при обработке аудио: {e}")
        await message.reply("Произошла ошибка при обработке аудиофайла.")