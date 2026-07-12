import json
from dataclasses import dataclass
from typing import Optional

from llm import chat
from memory.action import MemoryAction
from memory.models import Memory

@dataclass
class ValidatorResult:
    action : MemoryAction
    new_memory: Memory
    old_memory: Optional[Memory]
    reason : str


class MemoryValidator:
    def validate(self,new_memory: Memory,memories: list[Memory])-> ValidatorResult:
        prompt = f"""
        你是一名 Memory Validator。
            已有记忆：
            {memories}
            新的记忆(List格式)：
            {new_memory}
            请判断：
            1.ADD            
            2.UPDATE          
            3.MERGE           
            4.IGNORE   
            
            ADD表示新增一条记忆。
            UPDATE表示已有记忆被新的事实替换。
            MERGE表示两条记忆应该合并。
            IGNORE表示无需保存。
            
            如果 action 为 ADD，
            target_id 返回 null。
            如果 UPDATE，
            target_id 必须返回已有 Memory 的 id。
            如果 MERGE，
            target_id 返回要合并的 Memory id。
            如果 IGNORE，
            target_id 返回 null  
                 
            输出JSON格式,例：         
            {{
                "action":"",        
                "target_id":"",           
                "reason":""
            }}     
            """

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        response = chat(messages)
        content = json.loads(response.choices[0].message.content)
        print("validate_json_content:",content)
        old_memory = next(
            (memory for memory in memories if memory.id == content["target_id"]),
            None,
        )

        if content["action"] in ("UPDATE", "MERGE") and old_memory is None:
            raise ValueError("UPDATE/MERGE 必须指向已有记忆")

        return ValidatorResult(
            action=MemoryAction[content["action"]],
            new_memory=new_memory,
            old_memory=old_memory,
            reason=content["reason"],
        )
