import httpx
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def save_info_in_kb(text: str, chat_id: int):

    url = "https://mean-readers-lead.loca.lt/meetings/test/knowledgebase"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, json={"text": text}, timeout=30.0
        )
        response.raise_for_status()
        result = response.json()

    logging.info(f"Текст '{text}' успешно отправлен в БЗ")
    return result.get("text", text)

async def get_info_from_kb(query: str, chat_id: int):

    url = "https://api.maryrose.by/meetings/knowledge/search"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, json={"query": query, "limit": 5}, timeout=30.0
        )
        response.raise_for_status()
        logging.info(f"Текст '{query}' успешно получен из БЗ")
        return response.json()