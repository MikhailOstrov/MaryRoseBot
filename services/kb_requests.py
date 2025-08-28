import httpx
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def telegram_auth(email: str, chat_id: int):

    url = "https://maryrose.by/auth/telegram-auth"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, json={"email": email, "chat_id": chat_id}, timeout=30.0
        )
        response.raise_for_status()
    logging.info(f"Авторизаци успешна")

async def save_info_in_kb(text: str, chat_id: int):

    url = "https://maryrose.by/knowledge/add-text"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, json={"text": text, "chat_id": chat_id}, timeout=30.0
        )
        response.raise_for_status()
        result = response.json()

    logging.info(f"Текст '{text}' успешно отправлен в БЗ")
    return result.get("text", text)

async def get_info_from_kb(query: str, chat_id: int):

    url = "https://maryrose.by/meetings/knowledge/search"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, json={"query": query, "chat_id": chat_id}, timeout=30.0
        )
        response.raise_for_status()
        result = response.json()
    logging.info(f"Ответ от БЗ: {result}")

    if not result.get("success") or "results" not in result:
        return "По вашему запросу ничего не найдено"

    results = result["results"]

    if not results:
        return "По вашему запросу ничего не найдено"

    # Формируем красивый список
    message = "Результаты поиска:\n\n"
    for idx, r in enumerate(results, start=1):
        message += (
            f"📌 <b>{idx}. {r['title']}</b>\n"
            f"   {r['content_preview']}\n\n"
        )
    return message.strip()