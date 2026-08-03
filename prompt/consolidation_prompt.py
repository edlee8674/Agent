from memory.category import EXTRACTABLE_MEMORY_CATEGORIES, CATEGORY_DESCRIPTIONS
from memory.models import Memory


class ConsolidationPromptBuilder:
    def build(self, memories: list[Memory]) -> str:
        category_options = "\n".join(
                    f'- "{category.value}": {CATEGORY_DESCRIPTIONS[category]}'
                    for category in EXTRACTABLE_MEMORY_CATEGORIES
                )
        consolidation_prompt = f"""
        你是一个 Memory Consolidation Engine（记忆整合引擎）。
        
        你的任务是分析多个原子记忆（Atomic Memory），判断它们是否可以被整合为一个更高层次、更稳定的长期记忆（Consolidated Memory）。
        
        请严格遵守以下规则：
        
        1. 只能使用输入记忆中明确存在的信息。
        2. 不允许创造事实，不允许推测用户未明确表达的信息。
        3. 整合后的记忆应该表达稳定、长期、有价值的知识。
        4. 不要合并没有关联性的记忆。
        5. 如果这些记忆无法形成有意义的抽象，则返回 should_consolidate=false。
        6. 整合后的记忆必须保留原始记忆的核心含义，不改变事实。
        7. 输出内容应该简洁、客观，使用事实描述。
        8. 不要把一次性的事件、临时状态、短期行为转换为长期偏好或用户特征。
        
        整合后 memory 的 category 只能从以下值中选择：
        {category_options}
        
        以下记忆属于同一个候选分组，请分析这些记忆是否应该进行整合。
        
        记忆列表：
        
        {memories}
        
        请返回 JSON 格式结果：
        
        {{
          "should_consolidate": true,
          "memory": {{
            "fact": "用户计划在京都定居，并持续关注适合居住区域及商圈资源",
            "category": "future_plan",
            "importance": 0.9,
            "expires_at": null
          }},
          "source_memory_ids": ["id-1", "id-2", "id-3"],
          "reason": "这些记忆描述同一长期计划的不同细节"
        }}

        如果不应整合，返回：

        {{
          "should_consolidate": false,
          "reason": ""
        }}
        """

        return consolidation_prompt
