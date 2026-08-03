# AI Agent Memory Learning Project

一个从零实现 AI Agent Memory 的 Python 学习项目。当前重点是长期记忆的检索、写入、上下文预算、生命周期归档与分层架构。

## Current Capabilities

- Chat Completion 与 Structured Memory Extraction。
- Vector Memory：Embedding、Chroma 检索、SQLite Embedding Cache。
- Memory Validator：ADD / UPDATE / MERGE / IGNORE。
- Memory Reflection：ADD / UPDATE / DELETE / MERGE / ARCHIVE。
- Memory Ranking：相似度、重要性与时效性评分。
- Context Model、Token Budget、PromptBuilder 与简易 Context Compression。
- Memory Lifecycle：`expires_at`、时间衰减、ACTIVE / ARCHIVED 状态与 Chroma 状态过滤。
- Runtime State：SQLite 持久化、Reflection 与 Lifecycle 的时间门控。
- Dependency Injection、Bootstrap、Repository Pattern 与 Infrastructure Layer。

## Architecture

```text
main.py
  ↓
bootstrap.py
  ↓
MemoryApplication
  ├── Lifecycle gate → MemoryLifecycleService → Archive
  ├── ContextBuilder → Ranker → TokenBudget → Context
  ├── PromptBuilder → FinalTokenValidator → ContextCompressor
  ├── Extract → Validate → Merge → Write → Reflect
  ├── MemoryRepository → ChromaMemoryRepository
  └── RuntimeApplication → RuntimeStateStore
```

完整说明见 [ARCHITECTURE.md](ARCHITECTURE.md)。

## Quick Start

1. 创建并激活虚拟环境。

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 根据 `.env.example` 创建 `.env`：

```text
API_KEY=...
BASE_URL=...
CHAT_MODEL=...
EMBEDDING_MODEL=...
```

4. 运行：

```bash
python main.py
```

## Project Structure

```text
bootstrap.py              # Composition Root
main.py                   # 程序入口
context/                  # Context、Token budget、Prompt、Compression
memory/                   # Memory domain、application、pipeline、lifecycle、repository
infrastructure/           # Chroma repository、Embedding service、Token counter
runtime/                  # Scheduler、Runtime state、SQLite state store
```

## Lifecycle Notes

Memory 在领域层保存 `expires_at: date | None` 与 `status: MemoryStatus`。Chroma metadata 使用 ISO 日期字符串和 `"active"` / `"archived"`。

Lifecycle 当前不是常驻后台任务：每次构建 Context 时只进行时间门控判断；到达 `LIFECYCLE_INTERVAL_HOURS` 后才实际扫描并归档符合条件的 ACTIVE 记忆。

学习进度见 [ROADMAP.md](ROADMAP.md)，版本变化见 [CHANGELOG.md](CHANGELOG.md)，设计过程见 [DEVLOG.md](DEVLOG.md)。
