# AI Agent Memory Learning Project

一个从零实现 AI Agent Memory 的 Python 学习项目。当前重点是将长期记忆、上下文构建、Reflection 与运行状态组织为可替换的分层架构。

## Current Capabilities

- Chat Completion 与 Structured Memory Extraction
- Vector Memory：Embedding、Chroma 检索、SQLite Embedding Cache
- Memory Validator：ADD / UPDATE / MERGE / IGNORE
- Memory Reflection：ADD / UPDATE / DELETE / MERGE
- Runtime Scheduler 与 SQLite Runtime State
- Context Model、ContextBuilder、PromptBuilder
- Dependency Injection、Bootstrap、Repository Pattern

## Architecture

```text
main.py
  ↓
bootstrap.py
  ↓
MemoryApplication
  ├── ContextBuilder → Context → PromptBuilder
  ├── Memory Extract / Validate / Merge / Write / Reflect
  ├── MemoryRepository → ChromaMemoryRepository
  └── RuntimeApplication → RuntimeStateStore
```

详见 [ARCHITECTURE.md](ARCHITECTURE.md)。

## Quick Start

1. 创建并激活虚拟环境。

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 根据 `.env.example` 创建 `.env`，设置：

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
context/                  # Context model、ContextBuilder、PromptBuilder
memory/                   # Memory application、domain model、repository interface
infrastructure/           # Chroma repository、Embedding service
runtime/                  # Scheduler、Runtime state、SQLite state store
```

## Learning Progress

当前处于 Phase 2 的 Memory Module Refactoring：已完成 Context / Prompt pipeline 与 Repository + Infrastructure 拆分。下一步详见 [ROADMAP.md](ROADMAP.md)。
