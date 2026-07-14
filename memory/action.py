from enum import Enum


class MemoryAction(Enum):
    ADD = "add"

    UPDATE = "update"

    DELETE = "delete"

    IGNORE = "ignore"

    MERGE = "merge"
