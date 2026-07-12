from llm import chat
from memory.manager import build_context
from memory.extractor import extract_memory
from memory.manager import save_memory

user_input = input("User: ")

context = build_context(user_input)

messages = context + [
    {
     "role":"user",
     "content":user_input
    }
]

response = chat(messages)

assistant_content = response.choices[0].message.content

memories = extract_memory(user_input,assistant_content)

for memory in memories:
    print("extract_memory:",memory)
    if memory.importance > 0.5:
        save_memory(memory)


print("Bot: " + assistant_content)