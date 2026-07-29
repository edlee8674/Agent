# Architecture

本文档描述当前 Memory Engine 的分层结构与运行流程。

项目以 Application Layer 负责流程编排，业务规则、数据访问与外部技术实现分别位于独立层中。

---

## Layered Architecture

| Layer | Responsibility | Current modules |
| --- | --- | --- |
| Application | 编排用例与生命周期 | `memory/application.py`, `runtime/application.py`, `main.py` |
| Composition Root | 创建基础设施与组装依赖 | `bootstrap.py` |
| Domain | 表达 Memory 业务规则与结果模型 | `models.py`, `action.py`, `operation.py`, `extractor.py`, `validator.py`, `merger.py`, `reflection.py`, `scheduler.py` |
| Repository | 封装数据读写接口 | `vector_store.py`, `state_store.py`, `embedding_cache.py` |
| Infrastructure | 提供具体技术能力 | OpenAI-compatible API, ChromaDB, SQLite |

Application 只协调已有组件，不直接操作 Chroma 或 SQLite；Domain 组件通过构造函数接收 LLM 或 Repository 依赖，不自行创建外部客户端。

---

## Component Diagram

```text
main.py
  │
  ▼
bootstrap.create_memory_application
  ├── EmbeddingCache
  ├── LLMClient
  ├── MemoryRepository
  ├── RuntimeStateStore
  ├── RuntimeScheduler
  └── RuntimeApplication
          │
          ▼
MemoryApplication
  ├── LLMClient
  ├── MemoryExtractor
  ├── MemoryRetriever ──────► MemoryRepository ──────► ChromaDB
  ├── MemoryValidator ──────► LLMClient ─────────────► Chat / Embedding API
  ├── MemoryMerger ─────────► LLMClient
  ├── MemoryReflection ─────► LLMClient
  ├── MemoryWriter ─────────► MemoryRepository
  └── RuntimeApplication
        ├── RuntimeScheduler
        └── RuntimeStateStore ───────────────────────► SQLite

LLMClient ──────────────────────────────────────────► EmbeddingCache (SQLite)
```

---

## Application Layer

### `MemoryApplication`

`MemoryApplication` 是 Memory 用例的入口。它接收 Bootstrap 创建的依赖，不负责创建 OpenAI、Chroma 或 SQLite 客户端。

职责：

- 构建向量记忆上下文
- 提取并保存新 Memory
- 编排 Validator、Merger 与 Writer
- 根据 Runtime Scheduler 触发 Reflection
- 关闭 Runtime Store

关键方法：

```python
build_context(user_input)
extract_memory(user_input, assistant_content)
save_memory(memory)
run_reflection()
close()
```

### `RuntimeApplication`

`RuntimeApplication` 管理运行状态，而不依赖 Memory 模块。

职责：

- 加载与保存 `RuntimeState`
- 更新当前 Memory 数量
- 委托 `RuntimeScheduler` 判断是否需要 Reflection
- 在 Reflection 完成后更新反思基线、时间与次数

---

## Domain Layer

| Component | Responsibility |
| --- | --- |
| `Memory` | 记忆实体与 metadata 转换、TTL 判断 |
| `MemoryAction` | ADD、UPDATE、DELETE、IGNORE、MERGE 操作枚举 |
| `MemoryExtractor` | 从对话中提取结构化 `Memory` |
| `MemoryValidator` | 判断新 Memory 的写入动作与目标旧 Memory |
| `MemoryMerger` | 将两条 Memory 合成为一条更新后的 Memory |
| `MemoryReflection` | 为整个 Collection 生成 `ReflectionResult` |
| `MemoryOperation` / `ReflectionResult` | 表达 Reflection 的写入操作 |
| `RuntimeScheduler` | 按时间与新增 Memory 数量判断是否反思 |

`MemoryExtractor`、`MemoryValidator`、`MemoryMerger` 与 `MemoryReflection` 接收 `LLMClient`，但不拥有 OpenAI client 的创建逻辑。

---

## Repository and Infrastructure

### `MemoryRepository`

封装 Chroma Collection 的低层操作：

```python
add_memory(...)
query_memory(...)
update_memory(...)
delete_memory(...)
count_memories()
get_all_memories()
```

### `RuntimeStateStore`

使用 SQLite 保存唯一的 Runtime State：

- `memory_count`
- `last_reflection_time`
- `memory_count_after_reflection`
- `reflection_count`

### `LLMClient`

封装 Chat Completion 与 Embedding API，并通过 `EmbeddingCache` 缓存 Embedding 结果。

---

## Workflows

### 1. 回答前构建上下文

```text
User Input
  ↓
MemoryApplication.build_context
  ↓
MemoryRetriever.search_memory
  ↓
LLMClient.create_embedding
  ↓
MemoryRepository.query_memory
  ↓
Memory[] → System Context
```

### 2. 保存新记忆

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
RuntimeApplication.refresh_memory_count
  ↓
RuntimeScheduler.should_reflect
```

### 3. Reflection

```text
RuntimeScheduler returns True
  ↓
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
RuntimeApplication refreshes and persists RuntimeState
```

---

## Dependency Rules

```text
Bootstrap    → Infrastructure / Repository / Application
Application  → Domain / Repository
Domain      → Domain abstractions and injected dependencies
Repository  → Infrastructure libraries
Infrastructure → OpenAI SDK / ChromaDB / SQLite
```

`bootstrap.py` 是 Composition Root：它创建具体依赖并将它们注入 Application 与 Domain 组件。

`main.py` 是程序入口：调用 Bootstrap 创建 `MemoryApplication`，处理一次用户输入，并在 `finally` 中关闭 Runtime State Store。

`memory/manager.py` 不再承担工作流编排；当前仅导出 `MemoryApplication`，兼容旧模块路径。
