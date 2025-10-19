from datetime import datetime, timezone, timedelta
from config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt      
from config import logger



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











