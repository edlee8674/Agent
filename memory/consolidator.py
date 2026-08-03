import json

from llm import LLMClient
from memory.consolidation_result import ConsolidationResult
from memory.models import Memory
from prompt.consolidation_prompt import ConsolidationPromptBuilder


class MemoryConsolidator:
    def __init__(self, llm: LLMClient ,consolidation_prompt_builder: ConsolidationPromptBuilder):
        self.llm = llm
        self.consolidation_prompt_builder = consolidation_prompt_builder

    def consolidate(self, group: list[Memory]) -> ConsolidationResult | None:
        prompt = self.consolidation_prompt_builder.build(group)
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        response = self.llm.chat(messages)
        content = self._parse_json(response.choices[0].message.content)
        if not content.get("should_consolidate", False):
            return None

        memory_data = content.get("memory")
        source_memory_ids = content.get("source_memory_ids", [])
        if memory_data is None or len(set(source_memory_ids)) < 2:
            raise ValueError(
                "Consolidation result requires at least two distinct source_memory_ids"
            )

        group_ids = {memory.id for memory in group}
        if not set(source_memory_ids).issubset(group_ids):
            raise ValueError("Consolidation result contains a source id outside the candidate group")

        return ConsolidationResult(
            consolidated_memory=Memory.from_dict(memory_data),
            source_memory_ids=source_memory_ids,
            reason=content.get("reason", ""),
        )

    @staticmethod
    def _parse_json(content: str) -> dict:
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
                raise ValueError("Consolidation response does not contain JSON") from error
            try:
                return json.loads(content[start:end + 1])
            except json.JSONDecodeError as nested_error:
                raise ValueError("Consolidation response is not valid JSON") from nested_error
