from aiogram import Bot, Router, F
import json
from aiogram.types import Message

from config import dp, logger
from utils.chat_history import chat_history
from utils.llm_handler import get_response
from services.kb_requests import save_info_in_kb, get_info_from_kb

router = Router()

# Хендлер на текстовые сообщения
@router.message(F.text)
async def text_message_handler(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    user_text = message.text
    logger.info(f"Получено текстовое сообщение: '{user_text}' от {message.from_user.full_name}")

    response = await get_response(user_text, chat_id)

    data = json.loads(response)

    print(data) # Пока пусть будет, чтобы тестить

    key = int(data['key'])
    text_for_response = data['text']

    try:
        if key == 0:

            await save_info_in_kb(text_for_response, chat_id)
            await bot.send_message(chat_id, f"Сохранил твою информацию в БЗ")

        elif key == 1:

            info = await get_info_from_kb(text_for_response, chat_id)
            await bot.send_message(chat_id, f"{info}")

        elif key == 2:

            await bot.send_message(chat_id, f"{text_for_response}")

            # Логика сохранения истории чата
            if chat_id not in chat_history:
                chat_history[chat_id] = []

            chat_history[chat_id].append((user_text, text_for_response))

            if len(chat_history[chat_id]) > 15:
                chat_history[chat_id].pop(0)

            logger.info(f"Актуальная chat_history для {chat_id}: {chat_history.get(chat_id, [])}")
        else:
            logger.error(f"Ошибка обработки текста")
    except Exception as e:
        logger.error(f"Ошибка отправки текста на бэк: {e}")