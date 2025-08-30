from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F, Bot

from states.kb_states import SearchKnowledge
from services.kb_requests import get_info_from_kb
from utils.llm_handler import response_for_searh
from services.back_requests import send_audio_to_backend
from config import logger

router = Router()

# /search
@router.message(lambda message: message.text == "Найти знание")
async def start_search(message: Message, state: FSMContext):
    await message.answer("🔎 Введите запрос для поиска в базе знаний:")
    await state.set_state(SearchKnowledge.waiting_for_query)

@router.message(SearchKnowledge.waiting_for_query, F.text)
async def process_search(message: Message, state: FSMContext):
    search_text = await response_for_searh(message.text)
    result = await get_info_from_kb(search_text, message.chat.id)
    await message.answer(result)
    await state.clear()

@router.message(SearchKnowledge.waiting_for_text, F.voice | F.audio)
async def process_add_audio(message: Message, state: FSMContext, bot: Bot):
    chat_id = message.chat.id
    file_id = message.voice.file_id if message.voice else message.audio.file_id

    try:
        file_info = await bot.get_file(file_id)
        audio_bytes = await bot.download_file(file_info.file_path)
        response_audio = await send_audio_to_backend(audio_bytes, chat_id)
        
        search_text = await response_for_searh(response_audio)
        result = await get_info_from_kb(search_text, message.chat.id)
        await message.answer(result)
        await state.clear()
        
    except Exception as e:
        logger.error(f"Ошибка при обработке аудио: {e}")
        await message.reply("Произошла ошибка при обработке аудиофайла. Попробуйте еще раз.")