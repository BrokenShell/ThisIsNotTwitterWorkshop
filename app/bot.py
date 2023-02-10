import os
import openai
from dotenv import load_dotenv


def chat_bot(prompt: str) -> str:
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_KEY")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.01,
        presence_penalty=0.6,
    )
    result, *_ = response.choices
    return result.text.strip()
