# Architecture

本项目是一个学习型 AI Agent Memory Engine。当前架构使用分层设计、依赖注入与 Bootstrap 组合根，将流程编排、业务规则、Repository 接口和基础设施实现分开。

---

## Layers

| Layer | Responsibility | Current modules |
| --- | --- | --- |
| Entry | 接收一次用户输入并管理应用生命周期 | `main.py` |
| Composition Root | 创建具体依赖并完成注入 | `bootstrap.py` |
| Application | 编排 Memory、Runtime、Context 用例 | `memory/application.py`, `runtime/application.py` |
| Context | 组织上下文模型并构建 LLM messages | `context/models.py`, `context/builder.py`, `context/prompt_builder.py` |
| Domain | Memory 实体、规则与操作结果 | `memory/models.py`, `action.py`, `operation.py`, `extractor.py`, `validator.py`, `merger.py`, `reflection.py`, `scheduler.py` |
| Repository | 定义 Memory 数据访问接口 | `memory/repository.py` |
| Infrastructure | Chroma、Embedding、SQLite、LLM API 的具体实现 | `infrastructure/`, `llm.py`, `memory/embedding_cache.py`, `runtime/state_store.py` |

---

## Component Diagram

```text
main.py
  │
  ▼
bootstrap.create_memory_application
  ├── LLMClient ───────────────────────────────► Chat API
  ├── EmbeddingCache ──────────────────────────► SQLite
  ├── EmbeddingService ────────────────────────► Embedding API / Cache
  ├── ChromaMemoryRepository ──────────────────► ChromaDB
  ├── RuntimeStateStore ───────────────────────► SQLite
  ├── RuntimeScheduler
  └── MemoryApplication
        ├── ContextBuilder
        │     ├── MemoryRetriever
        │     ├── ShortMemory
        │     └── SummaryMemory
        ├── PromptBuilder
        ├── MemoryExtractor / Validator / Merger / Reflection
        ├── MemoryWriter
        └── RuntimeApplication
```

---

## Main Request Flow

```text
User input
  ↓
MemoryApplication.build_context
  ↓
ContextBuilder
  ├── MemoryRetriever.search_memory
  ├── ShortMemory.get
  └── SummaryMemory.get
  ↓
Context
  ↓
MemoryApplication.build_prompt
  ↓
PromptBuilder
  ↓
messages (system + user)
  ↓
LLMClient.chat
  ↓
Assistant response
```

`Context` 是 ContextBuilder 与 PromptBuilder 之间的数据模型，当前包含：

- `user_input`
- `memories`
- `short_memory`
- `summary_memory`

---

## Memory Persistence Flow

```text
Conversation
  ↓
MemoryExtractor
  ↓
MemoryApplication.save_memory
  ↓
MemoryRetriever.search_memory
  ↓
MemoryValidator
  ├── ADD / UPDATE / IGNORE ──► MemoryWriter
  └── MERGE ──► MemoryMerger ──► MemoryWriter (UPDATE)
  ↓
MemoryRepository
  ↓
ChromaMemoryRepository
  ↓
EmbeddingService + ChromaDB
  ↓
RuntimeApplication.refresh_memory_count
```

---

## Reflection Flow

```text
RuntimeScheduler.should_reflect
  ↓ true
MemoryApplication.run_reflection
  ↓
MemoryRetriever.get_all_memory
  ↓
MemoryReflection
  ↓
ReflectionResult
  ↓
MemoryWriter.apply
  ↓
RuntimeApplication updates and persists RuntimeState
```

---

## Repository and Infrastructure

### `MemoryRepository`

`MemoryRepository` 是面向 `Memory` 领域对象的抽象接口：

```python
add_memory(memory)
query_memory(text)
update_memory(memory_id, memory)
delete_memory(memory_id)
count_memories()
get_all_memories()
```

### `ChromaMemoryRepository`

Chroma 实现接收 `EmbeddingService`。上层只传入 `Memory` 或文本；Repository 内部生成 embedding，并转换为 Chroma 所需的 documents、metadatas 与 vectors。

### Runtime State

`RuntimeStateStore` 将以下运行状态写入 SQLite：

- 当前 Memory 数量
- 上次 Reflection 时间
- Reflection 后的 Memory 数量
- Reflection 次数

---

## Dependency Rules

```text
Bootstrap      → Infrastructure / Application
Application    → Domain / Context / Repository interface
Context        → Domain models and injected services
Infrastructure → Repository interface / OpenAI SDK / ChromaDB / SQLite
```

业务组件不直接创建 OpenAI、Chroma 或 SQLite 客户端；具体对象由 `bootstrap.py` 创建后注入。
