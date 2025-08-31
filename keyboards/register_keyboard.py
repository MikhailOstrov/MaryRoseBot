from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_webapp_keyboard(webapp_url: str, text: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопкой для перехода в Web App.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text=text,
        web_app=WebAppInfo(url=webapp_url)
    )
    return builder.as_markup()
