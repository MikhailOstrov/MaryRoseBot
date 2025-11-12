import aiohttp

from config import BACKEND_URL, INTERNAL_API_KEY

async def init_telegram_auth(telegram_user_id: int, session_id: str) -> str | None:
    """
    Отправляет запрос на бэкенд для инициации сессии регистрации.
    Возвращает URL для Web App или None в случае ошибки.
    """
    url = f"{BACKEND_URL}/auth/telegram-init"
    headers = {
        "X-Internal-API-Key": INTERNAL_API_KEY
    } 
    payload = {
        "telegram_user_id": telegram_user_id,
        "session_id": session_id
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("webapp_url")
                else:
                    # TODO: Добавить логирование ошибки
                    print(f"Error from backend: {response.status}")
                    return None
        except aiohttp.ClientError as e:
            # TODO: Добавить логирование ошибки
            print(f"Request failed: {e}")
            return None


async def init_telegram_login(telegram_user_id: int, session_id: str) -> str | None:
    """
    Отправляет запрос на бэкенд для инициации сессии АВТОРИЗАЦИИ.
    """
    url = f"{BACKEND_URL}/auth/telegram-init-login"
    headers = {
        "X-Internal-API-Key": INTERNAL_API_KEY
    }
    payload = {
        "telegram_user_id": telegram_user_id,
        "session_id": session_id
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("webapp_url")
                else:
                    print(f"Error from backend: {response.status}")
                    return None
        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")
            return None


async def create_referral_code(code: str, tariff_id: int) -> bool:
    """
    Отправляет запрос на бэкенд для создания нового реферального кода.
    Возвращает True в случае успеха, False в случае неудачи.
    """
    url = f"{BACKEND_URL}/referrals/"
    headers = {
        "X-Internal-API-Key": INTERNAL_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "tariff_id": tariff_id
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                # Успешное создание возвращает статус 201 Created
                if response.status == 201:
                    return True
                else:
                    print(f"Error from backend while creating referral code: {response.status} - {await response.text()}")
                    return False
        except aiohttp.ClientError as e:
            print(f"Request to create referral code failed: {e}")
            return False