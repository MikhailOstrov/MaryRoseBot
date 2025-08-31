from aiohttp import web
from aiogram import Bot
from utils.session_manager import session_manager
from config import INTERNAL_API_KEY, logger

async def handle_auth_success(request: web.Request):
    """
    Принимает webhook от основного бэкенда после успешной аутентификации пользователя.
    """
    # 1. Проверяем секретный ключ для безопасности
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {INTERNAL_API_KEY}":
        return web.Response(status=401, text="Unauthorized")

    # 2. Получаем session_id из тела запроса
    try:
        data = await request.json()
        session_id = data.get("session_id")
        if not session_id:
            return web.Response(status=400, text="Session ID is required")
    except Exception:
        return web.Response(status=400, text="Invalid JSON")

    # 3. Закрываем сессию и получаем данные (user_id, message_id)
    session = session_manager.close_session(session_id)
    if not session:
        logger.warning(f"Auth callback received for unknown or used session_id: {session_id}")
        return web.Response(status=404, text="Session not found or already used")

    # 4. Взаимодействуем с Telegram через объект бота
    bot: Bot = request.app['bot']
    try:
        # Удаляем сообщение с кнопкой "Войти в аккаунт"
        await bot.delete_message(chat_id=session.user_id, message_id=session.message_id)
        
        # Отправляем приветственное сообщение
        await bot.send_message(chat_id=session.user_id, text="✅ Добро пожаловать! Вы успешно авторизовались.")
        
        logger.info(f"Successfully processed auth for user {session.user_id}")
        return web.Response(status=200, text="OK")
    except Exception as e:
        logger.error(f"Error processing auth callback for user {session.user_id}: {e}")
        return web.Response(status=500, text="Internal server error")

def setup_webapp_routes(app: web.Application):
    """Добавляет роуты веб-приложения."""
    app.router.add_post('/auth-success', handle_auth_success)
