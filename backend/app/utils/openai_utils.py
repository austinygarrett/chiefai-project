import asyncio
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    return [item.embedding for item in response.data]

async def embed_texts_async(texts: list[str]) -> list[list[float]]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, embed_texts, texts)

def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def ask_gpt_with_context(question: str, context: str) -> str:
    prompt = f"""
        Government officials receive a daily briefing book. This includes a copy of the day’s schedule and memos prepared for each key item on the schedule.
        Memos can include logistics, background information, context about the participants, talking points, and more.
        You are assitant that is helping build the briefing book.

        Context:
        {context}

        Question:
        {question}

        Answer:
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()