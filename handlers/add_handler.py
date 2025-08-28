from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

from config import dp
from states.kb_states import AddKnowledge
from services.kb_requests import save_info_in_kb

router = Router()

# /add
@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await message.answer("📝 Введите текст, который нужно сохранить в базу знаний:")
    await state.set_state(AddKnowledge.waiting_for_text)

@router.message(AddKnowledge.waiting_for_text)
async def process_add(message: Message, state: FSMContext):

    await save_info_in_kb(message.text, message.chat.id)
    await state.clear()