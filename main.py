from openai import OpenAI

from config import API_KEY, BASE_URL, CHAT_MODEL
from memory.manager import build_context
from memory.extractor import extract_memory
from memory.manager import save_memory

openai_client  = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)
user_input = input("User: ")

context = build_context(user_input)

messages = context + [
    {
     "role":"user",
     "content":user_input
    }
]

response = openai_client.chat.completions.create(
    model=CHAT_MODEL,
    messages=messages
)

assistant_content = response.choices[0].message.content

memories = extract_memory(openai_client,user_input,assistant_content)

for memory in memories:
    print("extract_memory:",memory)
    if memory.importance > 0.5:
        save_memory(memory)


print("Bot: " + assistant_content)