# Architecture

本项目是一个学习型 AI Agent Memory Engine。当前采用分层设计、依赖注入和 Bootstrap 组合根：应用层编排流程，领域模块表达 Memory 规则，Repository 抽象数据访问，Infrastructure 提供 Chroma、SQLite 与 API 实现。

---

## Layers

| Layer | Responsibility | Current modules |
| --- | --- | --- |
| Entry | 接收一次用户输入、调用应用服务并关闭资源 | `main.py` |
| Composition Root | 创建具体依赖并完成注入 | `bootstrap.py` |
| Application | 编排上下文、记忆写入、Reflection 和 Lifecycle 用例 | `memory/application.py`, `runtime/application.py` |
| Context | 构建 Context、Token 预算、Prompt 与简易压缩 | `context/` |
| Domain | Memory 实体、状态、生命周期、排序及操作结果 | `memory/models.py`, `status.py`, `lifecycle.py`, `lifecycle_service.py`, `scoring.py`, `ranker.py`, `action.py`, `operation.py` |
| Repository | 定义面向 `Memory` 的数据访问接口 | `memory/repository.py` |
| Infrastructure | Chroma、Embedding、Token 计数、SQLite 与 LLM API | `infrastructure/`, `llm.py`, `memory/embedding_cache.py`, `runtime/state_store.py` |

`memory/manager.py` 仅保留对 `MemoryApplication` 的兼容导出，不承担流程编排。

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
  ├── TiktokenTokenCounter
  ├── ChromaMemoryRepository ──────────────────► ChromaDB
  ├── RuntimeStateStore ───────────────────────► SQLite
  ├── RuntimeScheduler
  └── MemoryApplication
        ├── ContextBuilder ──► MemoryRetriever / Ranker / TokenBudgetManager
        ├── PromptBuilder / ContextCompressor / FinalTokenValidator
        ├── MemoryExtractor / Validator / Merger / Reflection
        ├── MemoryWriter
        ├── MemoryLifecycleManager / MemoryLifecycleService
        └── RuntimeApplication
```

---

## Context and Request Flow

```text
User input
  ↓
MemoryApplication.build_context
  ↓
RuntimeScheduler.should_run_lifecycle
  ├── false ────────────────────────────────────────────────┐
  └── true → MemoryLifecycleService.process → archive writes │
                 ↓ RuntimeApplication.after_lifecycle        │
  ↓                                                           │
ContextBuilder                                                 │
  ├── MemoryRetriever.search_memory (ACTIVE only)             │
  ├── MemoryRanker                                             │
  ├── ShortMemory.get / SummaryMemory.get                     │
  └── TokenBudgetManager.apply                                │
  ↓                                                           │
Context ──► PromptBuilder ──► messages                         │
  ↓                                                           │
FinalTokenValidator                                            │
  ├── within limit → LLMClient.chat                            │
  └── over limit → ContextCompressor → rebuild messages ──────┘
```

`Context` 包含 `user_input`、排序后的长期记忆、短期记忆和摘要记忆。TokenBudgetManager 先按输入预算选择长期记忆；最终消息仍超限时，ContextCompressor 每次移除排序最低的一条长期记忆，再重新构建 Prompt。

---

## Memory Persistence Flow

```text
Conversation
  ↓
MemoryExtractor ──► Memory.create(ttl_days)
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
```

`Memory` 在领域层使用：

- `expires_at: date | None`：到期日期；`ttl_days` 仅在创建时用于计算它。
- `status: MemoryStatus`：当前包括 `ACTIVE` 和 `ARCHIVED`。

写入 Chroma 时，`expires_at` 和 `status` 分别序列化为 ISO 日期字符串和 `"active"` / `"archived"`。读取时再还原为领域类型；无 `status` 的旧记录默认视为 ACTIVE。

---

## Lifecycle and Archive Flow

```text
RuntimeScheduler.should_run_lifecycle
  ↓ true
MemoryLifecycleService.process
  ↓
MemoryRetriever.get_all_memory (ACTIVE only)
  ↓
MemoryLifecycleManager.should_archive
  ├── expires_at reached
  └── importance decay below threshold
  ↓
MemoryWriter.archive(memory_id)
  ↓
MemoryRepository.archive_memory(memory_id)
  ↓
Chroma metadata.status = "archived"
```

Lifecycle 当前由请求入口触发调度判断，而非独立后台进程：每次构建 Context 只检查是否到达间隔；只有到期时才扫描记忆。`RuntimeStateStore` 持久化 `last_lifecycle_run_time`，因此重启后仍能继续按间隔判断。

---

## Reflection Flow

```text
Save Memory
  ↓
RuntimeScheduler.should_reflect
  ↓ true
MemoryApplication.run_reflection
  ↓
MemoryReflection
  ↓
ReflectionResult (ADD / UPDATE / DELETE / MERGE / ARCHIVE)
  ↓
MemoryWriter.apply
  ↓
RuntimeApplication refreshes and persists RuntimeState
```

---

## Repository Contract

`MemoryRepository` 的当前主要接口：

```python
add_memory(memory)
query_memory(text, include_archived=False, top_k=3)
update_memory(memory_id, memory)
archive_memory(memory_id)
delete_memory(memory_id)
get_all_memories(include_archived=False)
count_memories()
```

`ChromaMemoryRepository` 在默认查询和读取全部记录时使用 `where={"status": "active"}`，使归档记忆不进入 Context、Ranking 与普通 Reflection 流程。

---

## Runtime State

`RuntimeStateStore` 使用 SQLite 保存：

- 当前 Memory 数量；
- 上次 Reflection 时间；
- Reflection 后的 Memory 数量；
- Reflection 次数；
- 上次 Lifecycle 执行时间。

数据库初始化时会检查并补加 `last_lifecycle_run_time` 列，以兼容已有 `runtime_state` 表。

---

## Dependency Rules

```text
Bootstrap      → Infrastructure / Application
Application    → Context / Domain / Repository interface
Context        → Domain models and injected services
Infrastructure → Repository interface / OpenAI SDK / ChromaDB / SQLite
```

业务组件不直接创建 OpenAI、Chroma 或 SQLite 客户端；具体对象由 `bootstrap.py` 创建后注入。
