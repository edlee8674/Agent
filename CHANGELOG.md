# Changelog

项目的重要功能和架构变更记录。

---

## v1.3.0 — 2026-07-30

### Context and Prompt Pipeline

#### Added

- `Context` 数据模型，包含用户输入、向量记忆、短期记忆与摘要记忆。
- `ContextBuilder`，负责汇总各类上下文来源。
- `PromptBuilder`，负责将 Context 转换为 LLM messages。
- `ShortMemory` 与 `SummaryMemory` 的 Context 接入。

#### Refactored

- `MemoryApplication` 接收并编排 `ContextBuilder`、`PromptBuilder`。
- `main.py` 通过 `MemoryApplication.build_context()` 和 `build_prompt()` 构建请求消息。

#### Fixed

- 修复 Bootstrap 注入 `context_builder` / `prompt_builder` 时与 Application 构造参数不一致的问题。
- 修复 Short Memory 消息字典在 Prompt 中格式化时的类型错误。
- 修复 `SummaryMemory.count_tokens()` 缺少 `self` 参数的问题。

---

## v1.2.0 — 2026-07-29

### Repository Pattern and Infrastructure Layer

#### Added

- `MemoryRepository` 领域数据访问接口。
- `ChromaMemoryRepository` 基础设施实现。
- `EmbeddingService`，负责 Embedding API 与 SQLite Cache。

#### Refactored

- Retriever 与 Writer 仅依赖 Repository 接口。
- Chroma 的字段转换、向量生成与 Collection 调用收敛到 `ChromaMemoryRepository`。
- Bootstrap 注入 `EmbeddingService` 与 `ChromaMemoryRepository`。

---

## v1.1.0 — 2026-07-21

### Application Layer and Dependency Injection

- 引入 `MemoryApplication` 与 `RuntimeApplication`。
- 引入 `bootstrap.py` 作为 Composition Root。
- Extractor、Retriever、Writer、Validator、Merger、Reflection 改为依赖注入的 class。
- Runtime State 持久化与 Reflection 调度进入 Application 流程。

---

## v1.0.0 — 2026-07-15

### Memory Reflection and Runtime State

- Memory Reflection、`ReflectionResult`、`MemoryOperation`。
- Runtime Scheduler、`RuntimeState`、SQLite `RuntimeStateStore`。
- Reflection 的 ADD、UPDATE、DELETE、MERGE 写入处理。

---

## v0.9.0 — 2026-07-12

### Memory Validation Pipeline

- `MemoryAction`、`ValidatorResult`、`MemoryValidator`、`MemoryMerger`。
- ADD、UPDATE、MERGE、IGNORE 的记忆写入决策。

---

## v0.1.0 – v0.8.0

- LLM Chat Completion、Prompt Engineering、Structured Output。
- Short Memory、Summary Memory、Token 处理。
- Embedding、向量检索、ChromaDB 与 SQLite Embedding Cache。
- Memory Extractor、TTL、Memory Writer、Memory Model。

---

## Next

- Memory Cleaner
- Memory Ranking
- TTL Cleaner
- Session Memory
