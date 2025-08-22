import asyncio
import logging
import os
from dotenv import load_dotenv
import string

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, FSInputFile 
from aiogram.enums import ParseMode

from utils.convert_audio import convert_audio_to_wav
from utils.backend_requests import send_audio_to_backend, send_text_to_backend
from knowledge_base.send_to_kb import send_text_to_kb

logging.basicConfig(level=logging.INFO)
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

dp = Dispatcher()

# Хендлер на команду /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Привет, {message.from_user.full_name}! Отправь мне текст или аудио.")

# Хендлер на команду /end
@dp.message(Command("end"))
async def command_end_handler(message: types.Message) -> None:

    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    await message.answer("Бот завершает свою работу. До свидания!")
    
    await dp.stop_polling()

# Хендлер на текстовые сообщения
@dp.message(F.text)
async def text_message_handler(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    text = message.text
    logging.info(f"Получено текстовое сообщение: '{text}' от {message.from_user.full_name}")

    try:
        response_text = await send_text_to_backend(text, chat_id)
        await bot.send_message(chat_id, f"{response_text}")
        await send_text_to_kb(response_text, chat_id)
    except Exception as e:
        logging.error(f"Ошибка отправки текста на бэк: {e}")

# Хендлер на аудио и голосовые сообщения
@dp.message(F.voice | F.audio)
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
        logging.info(f"Оригинальный файл сохранен: {original_ogg_path}")

        wav_path = convert_audio_to_wav(original_ogg_path)
        
        try:
            response_audio = await send_audio_to_backend(wav_path, chat_id)
            await bot.send_message(chat_id, f"{response_audio}")
        except Exception as e:
            logging.error(f"Ошибка отправки аудио на бэк: {e}")

    except Exception as e:
        logging.error(f"Ошибка при обработке аудио: {e}")
        await message.reply("Произошла ошибка при обработке аудиофайла.")

async def main() -> None:

    bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот был остановлен вручную.")