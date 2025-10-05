from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services import api_service
from keyboards.register_keyboard import get_webapp_keyboard
from utils.session_manager import session_manager

router = Router()

# Определяем состояния (дублируем для совместимости; лучше вынести в utils)
class AuthStates(StatesGroup):
    waiting_for_auth = State()  # Ожидание авторизации/регистрации
    authorized = State()        # Авторизовано

async def send_registration_link(user_id: int, message: Message, bot: Bot, state: FSMContext):
    """
    Универсальная функция для отправки ссылки на регистрацию.
    """
    await state.set_state(AuthStates.waiting_for_auth)  # Устанавливаем состояние ожидания
    
    # 1. Редактируем исходное сообщение, показывая статус
    await bot.edit_message_text(
        "Минутку, создаю безопасную ссылку...",
        chat_id=user_id,
        message_id=message.message_id
    )

    # 2. Создаем сессию
    session_id = session_manager.start_session(
        user_id=user_id,
        message_id=message.message_id
    )

    # 3. Получаем URL от бэкенда, передавая session_id
    webapp_url = await api_service.init_telegram_auth(user_id, session_id)

    if webapp_url:
        # 4. Снова редактируем сообщение, добавляя кнопку
        await bot.edit_message_text(
            text="Добро пожаловать! Для завершения регистрации, пожалуйста, нажмите на кнопку ниже.",
            chat_id=user_id,
            message_id=message.message_id,
            reply_markup=get_webapp_keyboard(webapp_url, text="✍️ Зарегистрироваться")
        )
    else:
        # 5. В случае ошибки, сообщаем об этом пользователю
        await bot.edit_message_text(
            text="К сожалению, произошла ошибка при попытке начать регистрацию. Попробуйте позже.",
            chat_id=user_id,
            message_id=message.message_id
        )


@router.message(Command("register"))
async def register_command_handler(message: Message, bot: Bot, state: FSMContext):
    """
    Обработчик команды /register.
    Инициирует процесс регистрации через Web App.
    """
    await send_registration_link(message.from_user.id, message, bot, state)


@router.callback_query(F.data == "register")
async def register_callback_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """
    Обработчик нажатия на инлайн-кнопку "Зарегистрироваться".
    """
    await callback.answer()  # Убираем "часики" на кнопке
    await send_registration_link(callback.from_user.id, callback.message, bot, state)

# Игнорирование всех сообщений в состоянии waiting_for_auth
@router.message(AuthStates.waiting_for_auth)
async def ignore_handler(message: Message, state: FSMContext):
    # Ничего не делаем — бот молчит, сообщение игнорируется
    pass