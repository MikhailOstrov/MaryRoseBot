import json
from datetime import datetime
from config import CLIENT_AS

date = datetime.now()

# Общая функция обработки сообщений пользователя
async def llm_response(user_text: str) -> str:
    
    instruction = f'''Ты умный ассистент Мэри по помощи в поиске и добавлении информации в векторных базах данных.
    Определи намерение пользователя по его сообщению, а именно, хочет ли он добавить информацию в базу знаний или же найти в ней информацию.
    Если пользователь хочет добавить информацию или же просит поставить напоминаниеы, то тебе нужно лишь занести её в базу знаний, не меняя текст пользователя, дай ответ в формате:
    {{"key": 0, "text": <текст>}}. Если же пользователь ищет информацию, то четко структурируй его вопрос, при надобности, и
    дай ответ в формате: {{"key": 1, "text": <запрос пользователя>}}. Если же пользователь пытается просто пообщаться с тобой, задает тебе обычные пустые
    вопросы, чтобы пообщаться или спрашивает что-то нецензурное, то скажи ему, что ты не предназначена для пустого общения и дай ответ в формате: 
    {{"key": 2, "text": <твой ответ>}}.'''
    
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

# После отрицательного результата поиска 
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
