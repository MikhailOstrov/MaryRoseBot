import httpx

from config import logger

async def telegram_auth(email: str, chat_id: int):

    url = "https://maryrose.by/auth/telegram-auth"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, json={"email": email, "chat_id": chat_id}, timeout=30.0
        )
        response.raise_for_status()
    logger.info(f"Авторизаци успешна")

async def save_info_in_kb(text: str, chat_id: int):
    url = "https://maryrose.by/knowledge/add-text"
    try:
        async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json={"text": text, "chat_id": chat_id}, timeout=30.0
                )
                response.raise_for_status()
                logger.info("Текст успешно добавлен в БЗ.")
                return "Текст успешно добавлен в БЗ."
    except Exception as e:
        logger.error(f"Произошла непредвиденная ошибка: {e}")
        return "Произошла ошибка на сервере, информация не добавлена. Исправим в ближайшее время, а пока, сохраните текст где-нибудь!"

async def get_info_from_kb(query: str, chat_id: int):
    url = "https://maryrose.by/knowledge/search"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json={"query": query, "chat_id": chat_id}, timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
        
        logger.info(f"Ответ от БЗ: {result}")

        if not result.get("success") or not result.get("results"):
            return None
        
        results = result["results"]
        
        message_parts = [
            f"📌 --- {idx}. {r['title']} ---\n   {r['content_preview']}\n"
            for idx, r in enumerate(results, start=1)
        ]
        return "Результаты поиска:\n\n" + "\n".join(message_parts).strip()

    except Exception as e:
         return "Произошла ошибка на сервере, информация не найдена. Исправим в ближайшее время!"