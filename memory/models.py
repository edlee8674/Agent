from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional
from uuid import uuid4

from memory.status import MemoryStatus


@dataclass
class Memory:
    id: str
    fact: str
    category: str
    importance: float
    created_time: str
    expires_at: date | None = None
    distance: Optional[float] = None
    status: MemoryStatus = MemoryStatus.ACTIVE

    def to_metadata(self):
        metedata = {
            "category": self.category,
            "importance": float(self.importance),
            "created_time": self.created_time,
            "status": self.status.value,
        }
        if self.expires_at is not None:
            metedata["expires_at"] = self.expires_at.isoformat()
        return metedata

    @classmethod
    def create(cls, fact: str, category: str, importance: float, ttl_days: int | None = None):
        expires_at = None
        if ttl_days is not None:
            expires_at = date.today() + timedelta(days=ttl_days)
        return cls(
            id=str(uuid4()),
            fact=fact,
            category=category,
            importance=importance,
            created_time=date.today().isoformat(),
            expires_at=expires_at,
            status=MemoryStatus.ACTIVE,
        )

    @classmethod
    def from_chroma(cls, id, document, metadata, distance, status=None):
        return cls(id=id,
                   fact=document,
                   category=metadata["category"],
                   importance=metadata["importance"],
                   expires_at=cls._parse_date(
                       metadata.get("expires_at", metadata.get("ttl"))
                   ),
                   created_time=metadata["created_time"],
                   distance=distance,
                   status=cls._parse_status(
                       status if status is not None else metadata.get("status")
                   )
                   )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id", str(uuid4())),
            fact=data["fact"],
            category=data["category"],
            importance=data["importance"],
            expires_at=cls._parse_date(data.get("expires_at", data.get("ttl"))),
            created_time=data.get("created_time") or date.today().isoformat(),
            distance=data.get("distance"),
            status=cls._parse_status(data.get("status")),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "fact": self.fact,
            "category": self.category,
            "importance": self.importance,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_time": self.created_time,
            "status": self.status.value,
        }

    def to_prompt(self):
        return self.fact

    def is_expired(self, today: date | None = None):
        if self.expires_at is None:
            return False
        today = today or date.today()
        return today >= self.expires_at

    @staticmethod
    def _parse_date(value: str | date | None) -> date | None:
        if value is None or isinstance(value, date):
            return value
        return date.fromisoformat(value)

    @staticmethod
    def _parse_status(value: str | MemoryStatus | None) -> MemoryStatus:
        if value is None:
            return MemoryStatus.ACTIVE
        if isinstance(value, MemoryStatus):
            return value
        return MemoryStatus(value)
