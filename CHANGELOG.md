# Changelog

项目的重要功能与代码结构变更记录。

---


## v1.1.0 — 2026-07-21

### Dependency Injection + Application Bootstrap

#### Added

- `Bootstrap`： 统一创建外部依赖并注入业务组件

#### Refactored

- `MemoryExtractor`、`MemoryRetriever`、`MemoryWriter`、`MemoryValidator`、`MemoryMerger`、`MemoryReflection` 改为接收依赖实例的 class。
- 业务组件不再自行创建 OpenAI client 或 Chroma client， 而是接收 Bootstrap 创建好的依赖。

#### Fixed

- 单元素 tuple 导致 LLMClient 调用失败

---


## v1.1.0 — 2026-07-21

### Application Layer Refactoring

#### Added

- `MemoryApplication`：编排上下文构建、记忆保存与 Reflection 流程。
- `RuntimeApplication`：编排运行状态加载、调度判断与持久化。
- `LLMClient`：统一 Chat Completion、Embedding 与 Embedding Cache。
- `MemoryRepository`：封装 Chroma 的增删改查与计数操作。

#### Refactored

- `MemoryExtractor`、`MemoryRetriever`、`MemoryWriter`、`MemoryValidator`、`MemoryMerger`、`MemoryReflection` 改为接收依赖实例的 class。
- `main.py` 通过 `MemoryApplication` 执行 Memory 流程。
- `RuntimeApplication` 不再反向依赖 Memory Retriever；Memory 数量由 Application Layer 传入。
- `memory/manager.py` 不再承担流程编排。

#### Fixed

- Reflection 后先重新统计 Memory 数量，再保存 Reflection 基线状态。
- 主程序使用 `try/finally` 关闭 Runtime State Store。

---

## v1.0.0 — 2026-07-15

### Memory Reflection and Runtime State

#### Added

- Memory Reflection、`ReflectionResult` 与 `MemoryOperation`。
- Runtime Scheduler、`RuntimeState` 与 SQLite `RuntimeStateStore`。
- Reflection 的 ADD、UPDATE、DELETE、MERGE 写入分发。

#### Fixed

- 支持 Chroma `query()` 的嵌套结果与 `get()` 的扁平结果转换为 `Memory`。
- 修复 Runtime State 的 SQLite 参数化查询与状态持久化。

---

## v0.9.0 — 2026-07-12

### Memory Validation Pipeline

#### Added

- `MemoryAction`、`ValidatorResult`、`MemoryValidator`、`MemoryMerger`。
- ADD、UPDATE、MERGE、IGNORE 的记忆写入决策。

#### Fixed

- Chroma distance 读取、TTL 兼容、Validator JSON f-string 与 Writer 参数传递错误。

---

## v0.8.0

### Embedding Cache

- 添加 SQLite Embedding Cache。
- 缓存命中时跳过 Embedding API 调用。

---

## v0.7.0

### Memory Architecture Refactoring

- 引入 `Memory` dataclass。
- 拆分 Retriever、Writer 与 Vector Store。
- 将 Memory 业务逻辑与 Chroma 数据访问分离。

---

## v0.1.0 – v0.6.0

- LLM Chat Completion、流式输出、Prompt Engineering。
- Short Memory、Summary Memory、Token 处理。
- Embedding、向量检索与 ChromaDB。
- Memory Extractor、重要性、分类、TTL。
- Memory Writer、保存、更新与去重。

---

## Next

- Memory Cleaner
- Memory Ranking
- TTL Cleaner
- Session Memory
- Prompt Builder
