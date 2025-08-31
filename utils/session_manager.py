import uuid
from typing import Dict, Any, Optional

class ActiveSession:
    """Простой класс для хранения данных сессии."""
    def __init__(self, user_id: int, message_id: int):
        self.user_id = user_id
        self.message_id = message_id

class SessionManager:
    """Управляет активными сессиями аутентификации в памяти."""
    def __init__(self):
        # В продакшене это лучше заменить на Redis
        self._sessions: Dict[str, ActiveSession] = {}

    def start_session(self, user_id: int, message_id: int) -> str:
        """Создает новую сессию и возвращает ее ID."""
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = ActiveSession(user_id=user_id, message_id=message_id)
        return session_id

    def update_message_id(self, session_id: str, message_id: int):
        """Обновляет message_id для существующей сессии."""
        if session_id in self._sessions:
            self._sessions[session_id].message_id = message_id

    def close_session(self, session_id: str) -> Optional[ActiveSession]:
        """Закрывает сессию по ID и возвращает ее данные."""
        return self._sessions.pop(session_id, None)

# Создаем единый экземпляр менеджера для всего приложения
session_manager = SessionManager()
