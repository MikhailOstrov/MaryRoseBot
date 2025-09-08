# MaryRoseBot/handlers/notification_handler.py
from aiohttp import web
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from config import INTERNAL_API_KEY, logger

async def handle_send_notification(request: web.Request):
    """
    Принимает запрос от основного бэкенда для отправки уведомления пользователю.
    """
    # 1. Проверяем внутренний API ключ
    auth_header = request.headers.get("Authorization")
    # Используем X-Internal-API-Key, как договаривались
    if not auth_header or auth_header != f"Bearer {INTERNAL_API_KEY}":
        logger.warning(f"Unauthorized attempt to access /send-notification from {request.remote}")
        return web.Response(status=401, text="Unauthorized")

    # 2. Получаем chat_id и message из тела запроса
    try:
        data = await request.json()
        chat_id = data.get("chat_id")
        message = data.get("message")
        if not chat_id or not message:
            return web.Response(status=400, text="chat_id and message are required")
    except Exception:
        return web.Response(status=400, text="Invalid JSON")

    # 3. Отправляем сообщение через объект бота
    bot: Bot = request.app['bot']
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=message
        )
        logger.info(f"Successfully sent notification to chat_id {chat_id}")
        return web.Response(status=200, text="OK")
    except TelegramAPIError as e:
        # Обрабатываем специфичные ошибки Telegram (например, если пользователь заблокировал бота)
        logger.error(f"Telegram API error while sending notification to {chat_id}: {e}")
        # Возвращаем ошибку, чтобы Celery мог, например, не пытаться повторить отправку
        return web.Response(status=400, text=f"Failed to send message: {e.message}")
    except Exception as e:
        logger.error(f"Unexpected error sending notification to {chat_id}: {e}")
        return web.Response(status=500, text="Internal server error")

def setup_notification_routes(app: web.Application):
    """Добавляет роут для приема уведомлений от бэкенда."""
    app.router.add_post('/send-notification', handle_send_notification)
