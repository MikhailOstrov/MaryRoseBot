import httpx
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def send_text_to_kb(text: str, chat_id: int):

    url = "https://mean-readers-lead.loca.lt/meetings/test/knowledgebase"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, json={"text": text}, timeout=30.0
        )
        response.raise_for_status()
        result = response.json()

    logging.info(f"Текст '{text}' успешно обработан на бэке")
    return result.get("text", text)