from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from uuid import uuid4


@dataclass
class Memory:
    id: str
    fact: str
    category: str
    importance: float
    ttl : Optional[int]
    created_time: str
    distance: Optional[float] = None

    def to_metadata(self):
        metedata = {
            "category": self.category,
            "importance": float(self.importance),
            "created_time": self.created_time

        }
        if self.ttl is not None:
            metedata["ttl"] = self.ttl
        return metedata

    @classmethod
    def create(cls, fact: str, category: str, importance: float, ttl: Optional[int] = None):
        return cls(id = str(uuid4()),
                   fact=fact,
                   category=category,
                   importance=importance,
                   ttl=ttl,
                   created_time = date.today().isoformat()
                   )
    @classmethod
    def from_chroma(cls, id, document, metadata, distance):
        return cls(id=id,
                   fact=document,
                   category=metadata["category"],
                   importance=metadata["importance"],
                   ttl=metadata["ttl"],
                   created_time=metadata["created_time"],
                   distance=distance
                   )

    def to_prompt(self):
        return self.fact

    def is_expired(self):
        if self.ttl is None:
            return False
        return date.today() > date.fromisoformat(days=self.ttl)