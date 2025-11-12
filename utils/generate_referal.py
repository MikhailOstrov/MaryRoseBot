from datetime import datetime, timezone, timedelta
from config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt      
from config import logger
import secrets
from services import api_service



def generate_token(code: str, referrer: str, hours: int = 24):
    """
    Генерирует инвайт-токен на основе настроек и аргументов командной строки.
    """
    try:
        logger.info(f"DEBUG: generate_token | Using SECRET_KEY starting with: {SECRET_KEY[:4] if SECRET_KEY else 'None'}")
        expire = datetime.now(timezone.utc) + timedelta(hours=hours)
        to_encode = {
            "exp": expire,
            "sub": code,  # Используем sub для хранения самого кода
            "type": "invite", # Добавляем тип, чтобы не спутать с токенами доступа
            "referrer": referrer
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return f"https://app.maryrose.by/signup?invite_token={encoded_jwt}"
        
    except Exception as e:
        return f"Error: {e}"


async def generate_refferal_code(tariff_id: int, code: str = None):
    """
    Генерирует (или использует существующий) реферальный код,
    регистрирует его в БД через API и возвращает готовую ссылку.
    """
    if not code:
        # Генерируем случайный 8-значный код, если не предоставлен собственный
        raise ValueError("Code is required")
    try:
        success = await api_service.create_referral_code(code=code, tariff_id=tariff_id)
        if success:
            return f"https://app.maryrose.by/signup?ref_code={code}"
        else:
            raise Exception("Failed to create referral code")
    except Exception as e:
        raise Exception(f"Failed to create referral code: {e}")











