
chat_history: dict[int, list[tuple[str, str]]] = {}  # Пока для хранения истории сообщений (15 пар: пользователь - LLM)

def format_chat_history_for_prompt(chat_id):
    history_formatted = ""
    for user_msg, bot_msg in chat_history.get(chat_id, []):
        history_formatted += f"Пользователь: {user_msg}\nБот: {bot_msg}\n"
    return history_formatted