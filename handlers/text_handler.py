from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import os
from aiogram import Bot

from config import logger
from utils.chat_history import chat_history
from utils.llm_handler import llm_response, llm_response_after_kb
from utils.convert_audio import convert_audio_to_wav
from services.back_requests import send_audio_to_backend
from services.kb_requests import get_info_from_kb, save_info_in_kb
from keyboards.inline_keyboard import decision

router = Router()

# Хендлер на текстовые сообщения
@router.message(F.text)
async def text_message_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_text = message.text
    logger.info(f"Получено текстовое сообщение: '{user_text}' от {message.from_user.full_name}")

    key, response = await llm_response(user_text)
    logger.info(f"Ответ от LLM: {key, response}")
    if key == 0:
        await save_info_in_kb(response, chat_id)
        await message.answer("Текст сохранен.")
    elif key == 1:
        info_from_kb = await get_info_from_kb(response, chat_id)
        if info_from_kb == None:
            await state.update_data(user_message=user_text)
            await message.answer("Не нашла информации в вашей базе знаний. Могу попытаться ответить сама. Нужен ли вам ответ?",
                reply_markup=decision)
        else:
            await message.answer(info_from_kb)

# Хендлер аудио и голосовые сообщения
@router.message(F.audio | F.voice)
async def text_message_handler(message: types.Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    logger.info(f"Получено аудио или голосовое сообщение от {message.from_user.full_name}")

    file_id = message.voice.file_id if message.voice else message.audio.file_id
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)

    temp_ogg_path = os.path.join(temp_dir, f"{file_id}.ogg")

    try:
        file_info = await bot.get_file(file_id)
        await bot.download_file(file_info.file_path, destination=temp_ogg_path)
        logger.info(f"Аудиофайл скачан в {temp_ogg_path}")

        wav_path = convert_audio_to_wav(temp_ogg_path)
        logger.info(f"Конвертация завершена. WAV-файл: {wav_path}")
        text_from_audio = await send_audio_to_backend(wav_path, chat_id)
        key, response = await llm_response(text_from_audio)

        await state.update_data(text_from_audio=text_from_audio)

        logger.info(f"Ответ от LLM: {key, response}")
        if key == 0:
            await save_info_in_kb(response, chat_id)
            await message.answer("Текст сохранен.")
        elif key == 1:
            info_from_kb = await get_info_from_kb(response, chat_id)
            if info_from_kb == None:
                await state.update_data(user_message=text_from_audio)
                await message.answer("Не нашла информации в вашей базе знаний. Могу попытаться ответить сама. Нужен ли вам ответ?",
                    reply_markup=decision)
            else:
                await message.answer(info_from_kb)
    except Exception as e:
        logger.error(f"Произошла ошибка при обработке аудио: {e}")

# Хендлер на колбэк "Yes"
@router.callback_query(F.data == "Yes")
async def answer_yes_callback(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    user_message = user_data.get("user_message") 

    if user_message:
        response = await llm_response_after_kb(user_message)
        await callback.message.edit_text(text=response, reply_markup=None)
    else:
        await callback.message.edit_text("Извините, произошла какая-то ошибка.", reply_markup=None)
    await state.clear()

@router.callback_query(F.data == "No")
async def auth_via_webapp_callback(callback: CallbackQuery):

    await callback.message.edit_text(
        text="Хорошо, можете продолжать работу.",
        reply_markup=None
    )

