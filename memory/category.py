from enum import Enum


class MemoryCategory(str, Enum):
    PREFERENCE = "preference"
    TEMPORARY_PREFERENCE = "temporary_preference"
    IDENTITY = "identity"
    FUTURE_PLAN = "future_plan"
    UNKNOWN = "unknown"


EXTRACTABLE_MEMORY_CATEGORIES = (
    MemoryCategory.PREFERENCE,
    MemoryCategory.TEMPORARY_PREFERENCE,
    MemoryCategory.IDENTITY,
    MemoryCategory.FUTURE_PLAN,
)


CATEGORY_DESCRIPTIONS = {
    MemoryCategory.PREFERENCE: "长期稳定偏好，例如“用户喜欢日本料理”。",
    MemoryCategory.TEMPORARY_PREFERENCE: "短期偏好，例如“用户近期想学习日语”。",
    MemoryCategory.IDENTITY: "稳定身份信息，例如“用户是产品经理”。",
    MemoryCategory.FUTURE_PLAN: "未来计划，例如“用户计划明年去北海道旅行”。",
}
