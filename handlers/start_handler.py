from aiogram.filters import CommandStart
from states.kb_states import  AuthStates
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from keyboards.reply_keyboard import main_menu
from keyboards.inline_keyboard import auth_keyboard
from services.kb_requests import telegram_auth

router = Router()

# /start
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"""👋 Привет, {message.from_user.full_name}! Для начала нужно войти в аккаунт.\nНажми ЗАРЕГИСТРИРОВАТЬСЯ, если ещё не имеешь аккаунта на основном сайте.\nНажми АВТОРИЗОВАТЬСЯ, если уже имеешь аккаунт:""",
        reply_markup=auth_keyboard
    )

# Нажал "Авторизоваться"
@router.callback_query(F.data == "auth")
async def auth_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✉️ Введите вашу почту для авторизации:")
    await state.set_state(AuthStates.waiting_for_email)
    await callback.answer()

# Обработка email
@router.message(AuthStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    chat_id = message.chat.id
    
    await telegram_auth(email, chat_id)

    await message.answer(f"✅ Авторизация успешна!\nТеперь можешь пользоваться базой знаний.",
        reply_markup=main_menu
    )
    await state.clear()