from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from states.kb_states import AddKnowledge
from services.kb_requests import save_info_in_kb

router = Router()

# /add
@router.message(lambda message: message.text == "Добавить знание")
async def start_add(message: Message, state: FSMContext):
    await message.answer("📝 Введите текст, который нужно сохранить в базу знаний:")
    await state.set_state(AddKnowledge.waiting_for_text)

@router.message(AddKnowledge.waiting_for_text)
async def process_add(message: Message, state: FSMContext):
    result = await save_info_in_kb(message.text, message.chat.id)
    await message.answer(result)
    await state.clear()