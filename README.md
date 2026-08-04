# AI Agent Memory Learning Project

一个从零实现 AI Agent Memory 的 Python 学习项目。当前重点是长期记忆的检索、写入、上下文预算、生命周期、遗忘、整合与分层架构。

## Current Capabilities

- Chat Completion 与 Structured Memory Extraction。
- Vector Memory：Embedding、Chroma 检索、SQLite Embedding Cache。
- Memory Validator：ADD / UPDATE / MERGE / IGNORE。
- Memory Reflection：ADD / UPDATE / DELETE / MERGE / ARCHIVE。
- Memory Ranking：相似度、重要性与时效性评分。
- Context Model、Token Budget、PromptBuilder 与简易 Context Compression。
- Memory Lifecycle：`expires_at`、`archived_at`、时间衰减、Archive、Forgetting、ACTIVE / ARCHIVED 状态与 Chroma 状态过滤。
- Memory Consolidation：候选分组、LLM 综合记忆生成、来源记忆归档。
- Runtime State：SQLite 持久化、Reflection、Lifecycle 与 Consolidation 的时间门控。
- Dependency Injection、Bootstrap、Repository Pattern 与 Infrastructure Layer。

## Architecture

```text
main.py
  ↓
bootstrap.py
  ↓
MemoryApplication
  ├── Lifecycle gate → Archive → Forgetting
  ├── Consolidation gate → Policy → Consolidator → Add + Archive
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
memory/                   # Memory domain、pipeline、lifecycle、forgetting、consolidation、repository
prompt/                   # Task prompt builders（如 Consolidation Prompt）
infrastructure/           # Chroma repository、Embedding service、Token counter
runtime/                  # Scheduler、Runtime state、SQLite state store
```

## Lifecycle Notes

Memory 在领域层保存 `expires_at`、`archived_at`、`MemoryStatus` 与 `MemoryCategory`。Chroma metadata 使用 ISO 日期字符串及对应的枚举字符串值。

Lifecycle 和 Consolidation 当前不是常驻后台任务：每次构建 Context 时只进行时间门控判断；达到各自间隔后才执行实际扫描。Lifecycle 负责 Archive 与 Forgetting；Consolidation 负责生成综合记忆并归档来源记忆。

学习进度见 [ROADMAP.md](ROADMAP.md)，版本变化见 [CHANGELOG.md](CHANGELOG.md)，设计过程见 [DEVLOG.md](DEVLOG.md)。
