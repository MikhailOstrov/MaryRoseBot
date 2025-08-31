from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot

from keyboards.inline_keyboard import auth_keyboard
from services import api_service
from keyboards.register_keyboard import get_webapp_keyboard
from utils.session_manager import session_manager


router = Router()

# /start
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"""👋 Привет, {message.from_user.full_name}! Для начала нужно войти в аккаунт.\nНажми зарегистрироваться, если ещё не имеешь аккаунта 
        на основном сайте.\nНажми авторизоваться, если уже имеешь аккаунт:""",
        reply_markup=auth_keyboard
    )

@router.callback_query(F.data == "auth")
async def auth_via_webapp_callback(callback: CallbackQuery, bot: Bot):
    """
    Обрабатывает нажатие кнопки "Авторизоваться", инициируя вход через Web App.
    """
    await callback.answer() # Убираем часики

    user_id = callback.from_user.id
    message = callback.message

    # 1. Редактируем исходное сообщение, показывая статус
    await bot.edit_message_text(
        "Подготовка страницы входа...",
        chat_id=user_id,
        message_id=message.message_id
    )

    # 2. Создаем сессию, используя ID отредактированного сообщения
    session_id = session_manager.start_session(
        user_id=user_id,
        message_id=message.message_id
    )

    # 3. Получаем URL от бэкенда
    webapp_url = await api_service.init_telegram_login(user_id, session_id)

    if webapp_url:
        # 4. Снова редактируем сообщение, добавляя кнопку
        await bot.edit_message_text(
            "Чтобы привязать ваш Telegram, пожалуйста, войдите в аккаунт на странице ниже.",
            chat_id=user_id,
            message_id=message.message_id,
            reply_markup=get_webapp_keyboard(webapp_url, text="🔑 Войти в аккаунт")
        )
    else:
        # 5. Сообщаем об ошибке
        await bot.edit_message_text(
            "Произошла ошибка. Попробуйте снова позже.",
            chat_id=user_id,
            message_id=message.message_id
        )