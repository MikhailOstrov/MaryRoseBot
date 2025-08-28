import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import dp, logger, API_TOKEN
from handlers import search_handler, start_handler, text_handler, audio_handler, add_handler

async def main():

    bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(add_handler.router)
    dp.include_router(search_handler.router)
    dp.include_router(start_handler.router)
    dp.include_router(audio_handler.router)
    dp.include_router(text_handler.router)

    await dp.start_polling(bot)

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот был остановлен вручную.")
