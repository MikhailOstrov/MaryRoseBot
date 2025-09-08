import asyncio
from aiogram import Bot
from aiohttp import web

from config import dp, logger, API_TOKEN
from handlers import start_handler, register_handler, message_handler
from handlers.web_auth_handler import setup_webapp_routes
from handlers.notification_handler import setup_notification_routes

async def main() -> None:

    bot = Bot(API_TOKEN)

    dp.include_router(start_handler.router)
    dp.include_router(register_handler.router)
    dp.include_router(message_handler.router)

    app = web.Application()
    app["bot"] = bot
    setup_webapp_routes(app)
    setup_notification_routes(app)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    logger.info("Webhook server started on http://0.0.0.0:8080")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот был остановлен вручную.")
