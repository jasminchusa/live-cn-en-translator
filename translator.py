import os
from dotenv import load_dotenv
load_dotenv()

PROVIDER = os.getenv('TRANSLATOR_PROVIDER','openai')

async def translate(text_cn: str) -> str:
    if not text_cn.strip():
        return ""
    if PROVIDER == 'openai':
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        model = os.getenv('OPENAI_MODEL','gpt-4o-mini')
        prompt = (
            "You are a realtime interpreter. Translate the user's Chinese speech to natural, concise spoken American English. "
            "Keep latency low, avoid filler, preserve tone. Only return the English.\nChinese:" + text_cn
        )
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    else:
        # Fallback: echo (for pipeline test)
        return text_cn
