import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, FSInputFile 
from aiogram.enums import ParseMode

# Загружаем переменные окружения
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Создаем объекты бота и диспетчера
# Диспетчер (Dispatcher) - главный роутер для обработки входящих событий (сообщений, команд и т.д.)
dp = Dispatcher()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

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
    """
    Этот хендлер будет принимать голосовые и аудио сообщения,
    скачивать их и отправлять обратно.
    """
    # Определяем, что пришло: голосовое или аудиофайл
    file_id = ""
    if message.voice:
        file_id = message.voice.file_id
        logging.info(f"Получено голосовое сообщение от {message.from_user.full_name}")
    elif message.audio:
        file_id = message.audio.file_id
        logging.info(f"Получен аудиофайл от {message.from_user.full_name}")

    # Создаем папку для загрузок, если ее нет
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    try:
        # Получаем информацию о файле
        file_info = await bot.get_file(file_id)
        # Формируем путь для сохранения
        file_path = os.path.join("downloads", file_info.file_path.split('/')[-1])

        # Скачиваем файл
        await bot.download_file(file_info.file_path, destination=file_path)
        logging.info(f"Файл сохранен по пути: {file_path}")
        await message.reply("Я получил и сохранил твое аудио. Сейчас отправлю его обратно.")

        # Отправляем аудиофайл обратно пользователю
        # FSInputFile - специальный класс для отправки файлов с диска
        audio_to_send = FSInputFile(file_path)

        if message.voice:
            # Отправляем как голосовое
            await bot.send_voice(chat_id=message.chat.id, voice=audio_to_send)
        elif message.audio:
            # Отправляем как аудио
            await bot.send_audio(chat_id=message.chat.id, audio=audio_to_send)

    except Exception as e:
        logging.error(f"Ошибка при обработке аудио: {e}")
        await message.reply("Произошла ошибка при обработке твоего аудиофайла.")


async def main() -> None:
    """
    Главная функция для запуска бота.
    """
    bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())