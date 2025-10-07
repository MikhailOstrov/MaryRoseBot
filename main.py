import asyncio
from aiogram import Bot
from aiohttp import web
from aiohttp.web_log import AccessLogger

from config import dp, logger, API_TOKEN
from handlers import start_handler, register_handler, message_handler, info_handler
from handlers.web_auth_handler import setup_webapp_routes
from handlers.notification_handler import setup_notification_routes

class CustomAccessLogger(AccessLogger):
    def log(self, request, response, time):
        # Не логируем health check запросы
        if request.path == "/health":
            return
        super().log(request, response, time)

async def health_check(request):
    """Простой эндпоинт для health check."""
    return web.Response(text="OK")

async def main() -> None:

    bot = Bot(API_TOKEN)
    
    dp.include_router(info_handler.router)
    dp.include_router(start_handler.router)
    dp.include_router(register_handler.router)
    dp.include_router(message_handler.router) 

    app = web.Application()
    app["bot"] = bot
    app.router.add_get("/health", health_check) # Добавляем эндпоинт
    setup_webapp_routes(app)
    setup_notification_routes(app)
    
    # Используем кастомный логгер
    runner = web.AppRunner(app, access_log_class=CustomAccessLogger)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    logger.info("Webhook server started on http://0.0.0.0:8080")
    logger.info("Lifespan: ----------------------------------------------- test docker")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот был остановлен вручную.")
