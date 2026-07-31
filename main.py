from bootstrap import create_memory_application

memory_app = create_memory_application()

try:
    user_input = input("User: ")

    context = memory_app.build_context(user_input)
    messages = memory_app.prepare_messages(context)
    response = memory_app.llm.chat(messages)
    assistant_content = response.choices[0].message.content
    memories = memory_app.extract_memory(user_input, assistant_content)

    for memory in memories:
        print("extract_memory:", memory)
        if memory.importance > 0.5:
            memory_app.save_memory(memory)
    print("Bot: " + assistant_content)

finally:
    memory_app.close()
