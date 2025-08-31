import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiohttp import web

from config import API_TOKEN
from handlers import start_handler, register_handler, add_handler, search_handler
from handlers.web_auth_handler import setup_webapp_routes

# Включаем логирование, чтобы видеть и ошибки, и информационные сообщения
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


async def main() -> None:
    # Инициализация бота и диспетчера
    bot = Bot(API_TOKEN)
    dp = Dispatcher()

    # Регистрируем роутеры
    dp.include_router(start_handler.router)
    dp.include_router(register_handler.router)
    dp.include_router(add_handler.router)
    dp.include_router(search_handler.router)

    # --- НАЧАЛО: Настройка и запуск веб-сервера ---
    
    # Создаем экземпляр веб-приложения
    app = web.Application()
    
    # Передаем экземпляр бота в веб-приложение, чтобы обработчики могли его использовать
    app["bot"] = bot
    
    # Настраиваем роуты для веб-хуков
    setup_webapp_routes(app)
    
    # Создаем и запускаем веб-сервер
    runner = web.AppRunner(app)
    await runner.setup()
    # Запускаем на 0.0.0.0, чтобы он был доступен извне (например, из Docker-контейнера бэкенда)
    # Порт 8080 - стандартный, его нужно будет указать в .env для бэкенда
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    logging.info("Webhook server started on http://0.0.0.0:8080")
    
    # --- КОНЕЦ: Настройка и запуск веб-сервера ---

    # Запускаем поллинг бота (удаляем старые обновления)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот был остановлен вручную.")
