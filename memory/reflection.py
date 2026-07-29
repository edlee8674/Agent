import json

from llm import LLMClient
from memory.action import MemoryAction
from memory.models import Memory
from memory.operation import MemoryOperation, ReflectionResult


class MemoryReflection:
    def __init__(self, llm: LLMClient):
        self.llm = llm


    def reflect(self, memories: list[Memory]) -> ReflectionResult:
        prompt = f"""
        你是一名 Memory Reflection Agent。
        你的职责不是提取新的记忆。
        也不是判断一条记忆是否保存。
        你的职责是整理整个 Memory Collection，
        让长期记忆保持：
        - 简洁
        - 准确
        - 不重复
        - 易于检索

        如果可以用一条更抽象的 Memory,替代多条具体 Memory，优先保留抽象 Memory。

        你可以执行以下操作：
        1.ADD
        创建新的抽象记忆。
        2.UPDATE
        修改已有记忆。
        3.DELETE
        删除无价值或过期记忆。
        4.MERGE
        将多个重复记忆合并。

        memories : {memories}

        只返回一个合法 JSON 对象，不要 Markdown 代码围栏、解释文字或省略号。
        如果不需要执行任何操作，返回：

        {{"operations": []}}

        返回 JSON 格式示例：

        {{
          "operations": [
            {{
              "action": "DELETE",
              "target_ids": ["123"],
              "reason": "已经过期"
            }},
            {{
              "action": "UPDATE",
              "target_ids": ["123"],
              "memory": {{
                "fact": "用户计划在北海道旅行",
                "category": "future_plan",
                "importance": 0.9,
                "ttl": null
              }},
              "reason": "补充了已有计划"
            }}
          ]
        }}
        """
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        response = self.llm.chat(messages)
        content = self._parse_json(response.choices[0].message.content)
        operations = []
        for op in content["operations"]:
            action = MemoryAction[op["action"]]
            memory = None
            memory_data = op.get("memory")
            if memory_data is not None:
                memory = Memory.from_dict(memory_data)
            operations.append(
                MemoryOperation(
                    action=action,
                    memory=memory,
                    target_ids=op.get("target_ids", []),
                    reason=op.get("reason", "")
                )
            )

        return ReflectionResult(operations=operations)

    @staticmethod
    def _parse_json(content: str):
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            content = content.rsplit("```", 1)[0].strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as error:
            start = content.find("{")
            end = content.rfind("}")
            if start == -1 or end == -1 or end <= start:
                raise ValueError("Reflection response does not contain JSON") from error
            try:
                return json.loads(content[start:end + 1])
            except json.JSONDecodeError as nested_error:
                raise ValueError("Reflection response is not valid JSON") from nested_error
