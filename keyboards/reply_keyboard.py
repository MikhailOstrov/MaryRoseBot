from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Основные кнопки на экране
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить знание")],
        [KeyboardButton(text="🔎 Найти знание")]
    ],
    resize_keyboard=True
)