import json
import uuid
from datetime import datetime
from memory.models import Memory

def extract_memory(client, user_input,assistant_content):

    prompt = f"""
你是一个 Memory Extractor。
你的任务是从用户聊天中提取未来有价值的信息。
只提取事实，不保存AI建议。
输出JSON
请判断下面的信息是否值得在未来聊天中继续使用。

包括但不限于：

- 用户长期偏好
- 用户身份、职业
- 用户长期习惯
- 用户未来已经确定的计划、愿望
- 用户明确表达希望记住的信息
- 对以后回答有帮助的重要事实

不要保存：

- AI生成内容
- 一次性的执行过程
- 无意义闲聊

注意：
不要重复已有事实。
如果表达相同，
请返回同一条。

如果需要保存，返回：

{{
"memories":[
    {{
        "fact":"",
        "category":"preference",
        "importance":0.8,
        "ttl":null
    }}
]
}}

字段解释：
fact
真正保存内容。
category
决定生命周期。
importance
重要程度。
ttl
过期时间。ttl 请根据当前日期开始计算。


用户输入：

{user_input}

AI回答：
{assistant_content}

"""

    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )
    content = response.choices[0].message.content

    data = json.loads(content)

    memories = []

    for item in data["memories"]:
        memories.append(
            Memory.create(
                fact=item["fact"],
                category=item["category"],
                importance=item["importance"],
                ttl=item["ttl"],
            )
        )

    return memories