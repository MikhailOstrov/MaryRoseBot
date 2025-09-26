import httpx

from config import logger, INTERNAL_API_KEY, BACKEND_URL

async def telegram_auth(email: str, chat_id: int):

    url = f"{BACKEND_URL}/auth/telegram-auth"
    headers = {"X-Internal-Api-Key": INTERNAL_API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, headers=headers, json={"email": email, "chat_id": chat_id}, timeout=30.0
        )
        response.raise_for_status()
    logger.info(f"Авторизация успешна")

async def save_info_in_kb(text: str, chat_id: int):
    url = f"{BACKEND_URL}/knowledge/add-text"
    headers = {"X-Internal-Api-Key": INTERNAL_API_KEY}
    try:
        async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, headers=headers, json={"text": text, "chat_id": chat_id}, timeout=30.0
                )
                response.raise_for_status()
                logger.info("Текст успешно добавлен в БЗ.")
                return "Текст успешно добавлен в БЗ."
    except Exception as e:
        logger.error(f"Произошла непредвиденная ошибка: {e}")
        return "Произошла ошибка на сервере, информация не добавлена. Исправим в ближайшее время, а пока, сохраните текст где-нибудь!"

async def get_info_from_kb(query: str, chat_id: int):
    url = f"{BACKEND_URL}/knowledge/search"
    headers = {"X-Internal-Api-Key": INTERNAL_API_KEY}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, headers=headers, json={"query": query, "chat_id": chat_id}, timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
        
        logger.info(f"Ответ от БЗ: {result}")

        if not result.get("success") or not result.get("results"):
            return None
        
        results = result["results"]
        
        message_parts = [
            f"📌  {idx}. {r['title']} \n   {r['content_preview']}\n"
            for idx, r in enumerate(results, start=1)
        ]
        return "Результаты поиска:\n\n" + "\n".join(message_parts).strip()

    except Exception as e:
         return "Произошла ошибка на сервере, информация не найдена. Исправим в ближайшее время!"
    
async def check_limit_in_kb(chat_id: int):
    url = f"{BACKEND_URL}/knowledge/check-limit"
    headers = {"X-Internal-Api-Key": INTERNAL_API_KEY}
    try:
        async with httpx.AsyncClient() as client:
                count = await client.post(
                    url, headers=headers, json={"chat_id": chat_id}, timeout=30.0
                )
                count.raise_for_status()
                logger.info(f"Оставшееся количество записей {count}")
                if count <= 5:
                     return 1, "У вас осталось менее 5 записей. Реструктурируйте ваши записи в БЗ. В ином случае некоторая информация может не попасть в БЗ."
                elif count == 0:
                    return 2,"Вы достигли лимита записей."
                else:
                     return 0, None
    except Exception as e:
        logger.error(f"Произошла непредвиденная ошибка: {e}")
        return "Произошла ошибка на сервере, информация не добавлена. Исправим в ближайшее время, а пока, сохраните текст где-нибудь!"