from openai import AsyncOpenAI
import os
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv() 

# Клиент OpenAI
CLIENT_AS = AsyncOpenAI(
    api_key=os.getenv("PROXY_API"),
    base_url=os.getenv("BASE_OPENAI_URL"),
)

now = datetime.now()

date = now.strftime("%d.%m.%Y")

async def llm_response(user_text: str) -> str:
    
    instruction = f'''Ты умный ассистент Мэри по помощи в поиске и добавлении информации в векторных базах данных.
    Определи намерение пользователя по его сообщению, а именно, хочет ли он добавить информацию в базу знаний или же найти в ней информацию.
    Если пользователь хочет добавить информацию, то тебе нужно лишь занести её в базу знаний, не меняя текст пользователя, дай ответ в формате:
    {{"key": 0, "text": <текст>}}. Если же пользователь ищет информацию, то четко структурируй его вопрос при надобности и
    дай ответ в формате: {{"key": 1, "text": <запрос пользователя>}}. Сегодня {date}. Учитывай это при занесении информации.
    Например, если пользователь просит записать созвон на завтра на 14:00 - следовательно, запись должна быть:
    Созвон 03.09.2025 в 14:00.'''

    chat_completion = await CLIENT_AS.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": user_text}
        ]
    )
    try:
        response_dict = json.loads(chat_completion.choices[0].message.content)

        key_value = response_dict.get('key')
        text_value = response_dict.get('text')

    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
    return key_value, text_value

async def llm_response_after_kb(user_text: str) -> str:
    
    instruction = f'''Ты умный ассистент Мэри. Максимально точно попробуй ответить на этот вопрос.
    Если ты не уверена, что сможешь правильно ответить, скажи об этом. Будь очень строгой по разговору.
    Если тебе задают вопрос не по делу, то есть какое-либо приветствие или бессмысленные вопросы по отношению
    к тебе, то ответь, что вопрос не по формату разговора.'''

    chat_completion = await CLIENT_AS.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": user_text}
        ]
    )

    return chat_completion.choices[0].message.content
