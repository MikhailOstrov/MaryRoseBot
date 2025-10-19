from datetime import datetime, timezone, timedelta
from config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

def generate_token(code: str, referrer: str, hours: int = 24):
    """
    Генерирует инвайт-токен на основе настроек и аргументов командной строки.
    """
    try:
        expire = datetime.now(timezone.utc) + timedelta(hours=hours)
        to_encode = {
            "exp": expire,
            "sub": code,  # Используем sub для хранения самого кода
            "type": "invite", # Добавляем тип, чтобы не спутать с токенами доступа
            "referrer": referrer
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return f"https://app.maryrose.by/signup?invite_token={encoded_jwt}\n"
        
    except Exception as e:
        return f"Error: {e}"











