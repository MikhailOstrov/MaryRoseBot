from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from config import dp
from states.kb_states import SearchKnowledge
from services.kb_requests import get_info_from_kb

router = Router()

# /search
@router.message(lambda message: message.text == "🔎 Найти знание")
async def start_search(message: Message, state: FSMContext):
    await message.answer("🔎 Введите запрос для поиска в базе знаний:")
    await state.set_state(SearchKnowledge.waiting_for_query)

@router.message(SearchKnowledge.waiting_for_query)
async def process_search(message: Message, state: FSMContext):

    await get_info_from_kb(message.text, message.chat.id)
    await state.clear()