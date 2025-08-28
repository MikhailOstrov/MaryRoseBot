from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from config import logger
from utils.chat_history import chat_history
from states.kb_states import AddKnowledge, SearchKnowledge
from utils.llm_handler import basic_response

router = Router()

# Хендлер на текстовые сообщения
@router.message(F.text)
async def text_message_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_text = message.text

    logger.info(f"Получено текстовое сообщение: '{user_text}' от {message.from_user.full_name}")

    current_state = await state.get_state()
    if current_state in (AddKnowledge.waiting_for_text, SearchKnowledge.waiting_for_query):
        return
    
    response = await basic_response(user_text, chat_id)

    await message.answer(response)

    # Логика сохранения истории чата
    if chat_id not in chat_history:
        chat_history[chat_id] = []

    chat_history[chat_id].append((user_text, response))

    if len(chat_history[chat_id]) > 15:
        chat_history[chat_id].pop(0)

    logger.info(f"Актуальная chat_history для {chat_id}: {chat_history.get(chat_id, [])}")