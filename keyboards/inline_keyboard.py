from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

auth_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Зарегистрироваться", url="https://maryrose.by/signup"),
            InlineKeyboardButton(text="🔑 Авторизоваться", callback_data="auth")
        ]
    ]
)
