# Changelog

项目的重要功能和架构变更记录。

---

## v1.6.0 — 2026-08-04

### Memory Forgetting and Consolidation

#### Added

- `archived_at`：记录记忆归档日期。
- Forgetting 规则：归档保留期、低衰减值、可遗忘 Category 三项同时满足时物理删除记忆。
- `MemoryCategory` 与 Extractor / Merger / Reflection 的统一类别约束。
- `ConsolidationPromptBuilder`、`ConsolidationPolicy`、`MemoryConsolidator`、`ConsolidationResult`、`MemoryConsolidationService`。
- Consolidation 时间门控：`last_consolidation_time`、`should_run_consolidation()`、`after_consolidation()`。
- `MIN_CONSOLIDATION_GROUP_SIZE` 与 `CONSOLIDATION_INTERVAL_HOURS` 配置。

#### Changed

- Archive 同时持久化 `status="archived"` 与 `archived_at`。
- Lifecycle 先归档符合条件的 ACTIVE 记忆，再检查包含 ARCHIVED 的集合进行 Forgetting。
- Consolidation 先新增综合记忆，再归档来源记忆，避免新增失败时丢失来源信息。
- Runtime SQLite State 增加 consolidation 时间列及兼容迁移。

#### Fixed

- 修复 Category 未受 Prompt/领域模型约束导致 Lifecycle 类别规则无法匹配的问题。
- 修复 Consolidation Prompt 未插入候选记忆、Consolidator 缺少 JSON 解析与 `should_consolidate=false` 分支的问题。
- 修复 RuntimeState 未持久化 consolidation 时间、重启后重复执行 Consolidation 的问题。

---

## v1.5.0 — 2026-08-03

### Memory Lifecycle and Archive

#### Added

- `MemoryStatus`：`ACTIVE` 与 `ARCHIVED` 状态。
- `MemoryLifecycleManager`：过期判断、时间衰减与归档判断。
- `MemoryLifecycleService`：扫描当前 ACTIVE 记忆并执行归档。
- `MemoryAction.ARCHIVE` 与 Reflection ARCHIVE 操作处理。
- Runtime 生命周期调度状态：`last_lifecycle_run_time`、`should_run_lifecycle()`、`after_lifecycle()`。

#### Changed

- TTL 领域字段改为 `expires_at`；`ttl_days` 仅作为创建 Memory 时的相对天数输入。
- Chroma metadata 保存 `expires_at` ISO 字符串与 `status` 字符串。
- Repository 新增 `archive_memory()`，查询和读取全部记忆支持 `include_archived`。
- Chroma 默认通过 `where={"status": "active"}` 排除归档记忆。
- Lifecycle 由 Context 构建入口进行时间门控，而非每次请求都执行全量扫描。

#### Fixed

- 修复日期字符串未还原为 `date` 时无法进行过期比较的问题。
- 修复 status 枚举不能直接写入 Chroma / JSON、旧记录缺少 status 时无法读取的问题。
- 修复 ARCHIVE 操作错误要求完整 Memory，而不是只按目标 ID 更新状态的问题。

---

## v1.4.0 — 2026-07-31

### Ranking and Context Compression

#### Added

- `MemoryScorer` 与 `MemoryRanker`：基于相似度、重要性、时效性进行排序。
- `TokenBudgetManager` 与 `TokenBudgetConfig`：为输入上下文分配 Token 预算。
- `ContextCompressor` 与 `FinalTokenValidator`：最终消息超限时执行简易长期记忆压缩。
- `TiktokenTokenCounter` 基础设施实现。

#### Fixed

- 修复将 `MemoryValidator` 当作可调用 Token 校验器使用的问题。
- 修复将 Prompt messages 当作 Context 访问的问题。
- 修复最终 Token 校验器错误调用 TokenCounter 的问题。

---

## v1.3.0 — 2026-07-30

### Context and Prompt Pipeline

- 引入 `Context`、`ContextBuilder`、`PromptBuilder`。
- `MemoryApplication` 负责 Context 与 Prompt 的用例编排。
- 接入 Short Memory、Summary Memory、向量记忆。

---

## v1.2.0 — 2026-07-29

### Repository Pattern and Infrastructure Layer

- 引入 `MemoryRepository` 与 `ChromaMemoryRepository`。
- 引入 `EmbeddingService`，负责 Embedding API 与 SQLite Cache。
- Retriever 与 Writer 改为依赖 Repository 接口。

---

## v1.1.0 — 2026-07-21

### Application Layer and Dependency Injection

- 引入 `MemoryApplication`、`RuntimeApplication` 与 `bootstrap.py`。
- Extractor、Retriever、Writer、Validator、Merger、Reflection 改为依赖注入的 class。
- 引入 Runtime State 持久化与 Reflection 调度。

---

## v1.0.0 — 2026-07-15

### Memory Reflection and Runtime State

- Memory Reflection、`ReflectionResult`、`MemoryOperation`。
- Reflection 的 ADD、UPDATE、DELETE、MERGE 写入处理。

---

## v0.9.0 — 2026-07-12

### Memory Validation Pipeline

- `MemoryAction`、`ValidatorResult`、`MemoryValidator`、`MemoryMerger`。
- ADD、UPDATE、MERGE、IGNORE 的记忆写入决策。

---

## v0.1.0 – v0.8.0

- LLM Chat Completion、Structured Output 与 Prompt Engineering。
- Short Memory、Summary Memory、Embedding、ChromaDB。
- SQLite Embedding Cache、Memory Extractor、Memory Writer。
