from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from utils.chat_history import format_chat_history_for_prompt
load_dotenv() 

# Клиент OpenAI
CLIENT_AS = AsyncOpenAI(
    api_key=os.getenv("PROXY_API"),
    base_url=os.getenv("BASE_OPENAI_URL"),
)

async def basic_response(user_text: str, chat_id: int) -> str:
    
    basic_response = f'''Ты умный ассисент по имени Мэри. Отвечай подробно и четко, чтобы хорошо доносить информацию до пользовател. Используй
    историю вашего чата, если она есть, чтобы понимать, о чем идет речь при длительном разговоре с пользователем: {format_chat_history_for_prompt(chat_id)}.
    '''

    chat_completion = await CLIENT_AS.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": basic_response},
            {"role": "user", "content": user_text}
        ]
    )
    return chat_completion.choices[0].message.content

async def response_for_searh(user_text: str) -> str:
    
    response_for_searh = '''Ты умный ассистент по помощи в поиске информации по векторным базам данных.
    Сформулируй текст так, чтобы отправить его в базу данных и получить релевантные ответы.'''

    chat_completion = await CLIENT_AS.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": response_for_searh},
            {"role": "user", "content": user_text}
        ]
    )
    return chat_completion.choices[0].message.content