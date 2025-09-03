from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

auth_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Зарегистрироваться", callback_data="register"),
            InlineKeyboardButton(text="🔑 Авторизоваться", callback_data="auth")
        ]
    ]
)

decision = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=" Да ", callback_data="Yes"),
            InlineKeyboardButton(text=" Нет ", callback_data="No")
        ]
    ]
)
