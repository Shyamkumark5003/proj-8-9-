import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
_client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
    timeout=300,
)


def embed(text: str) -> list:
    r = _client.embeddings.create(model=os.getenv("EMBED_MODEL"), input=text)
    return r.data[0].embedding


def chat(system: str, user: str) -> str:
    r = _client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        temperature=0,
        extra_body={"reasoning_effort": "none"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return (r.choices[0].message.content or "").strip()