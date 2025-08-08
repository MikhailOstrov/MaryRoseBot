import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, FSInputFile 
from aiogram.enums import ParseMode

from utils.convert_audio import convert_audio_to_wav

logging.basicConfig(level=logging.INFO)
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

# Хендлер на команду /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Этот хендлер будет вызван на команду /start
    """
    await message.answer(f"Привет, {message.from_user.full_name}! Отправь мне текст или аудио.")

# Хендлер на текстовые сообщения
@dp.message(F.text)
async def text_message_handler(message: Message) -> None:
    """
    Этот хендлер будет принимать и анализировать текстовые сообщения.
    """
    text = message.text
    logging.info(f"Получено текстовое сообщение: '{text}' от {message.from_user.full_name}")

    # Ваша логика анализа текста
    if "привет" in text.lower():
        response = "Привет! Рад тебя видеть."
    elif "пока" in text.lower():
        response = "До скорой встречи!"
    else:
        response = f"Ты написал: '{text}'. Я запомнил это."

    await message.answer(response)

# Хендлер на аудио и голосовые сообщения
@dp.message(F.voice | F.audio)
async def audio_message_handler(message: Message, bot: Bot) -> None:

    file_id = message.voice.file_id if message.voice else message.audio.file_id
    
    # Создаем папки для загрузок и конвертаций, если их нет
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    if not os.path.exists("converted"):
        os.makedirs("converted")

    try:

        file_info = await bot.get_file(file_id)
        original_ogg_path = os.path.join("downloads", file_info.file_path.split('/')[-1])
        await bot.download_file(file_info.file_path, destination=original_ogg_path)
        logging.info(f"Оригинальный файл сохранен: {original_ogg_path}")

        await message.reply("Аудио получено. Начинаю конвертацию...")

        wav_path = convert_audio_to_wav(original_ogg_path)

        await message.reply(f"Файл успешно сохранен в форматах MP3 и WAV в папке 'converted'.")
        
        mp3_to_send = FSInputFile(wav_path)
        await bot.send_audio(chat_id=message.chat.id, audio=mp3_to_send)

    except Exception as e:
        logging.error(f"Ошибка при конвертации аудио: {e}")
        await message.reply("Произошла ошибка при обработке вашего аудиофайла. Убедитесь, что FFmpeg установлен.")


async def main() -> None:
    """
    Главная функция для запуска бота.
    """
    bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())