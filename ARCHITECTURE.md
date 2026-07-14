# Architecture

This document describes the current architecture of the Memory Engine.

The project follows a layered design where each module has a single responsibility.

---

# High-Level Architecture

```text
                    User
                      │
                      ▼
                MemoryManager
                      │
      ┌───────────────┴────────────────┐
      │                                │
      ▼                                ▼
 PromptBuilder                 Memory Pipeline
      │                                │
      ▼                                ▼
     LLM                        MemoryExtractor
      │                                │
      ▼                                ▼
 Assistant Response          MemoryRetriever
                                      │
                                      ▼
                               MemoryValidator
                                      │
                                      ▼
                              ValidationResult
                                      │
                                      ▼
                                MemoryWriter
                                      │
                                      ▼
                              RuntimeScheduler
                                      │
                     should_reflect(state)?
                          │            │
                        No             Yes
                          │            ▼
                          │     MemoryReflection
                          │            │
                          │            ▼
                          │    ReflectionResult
                          │            │
                          └────────► MemoryWriter
                                       │
                                       ▼
                                  VectorStore
                                       │
                                       ▼
                                    ChromaDB
```

---

# Module Responsibilities

## MemoryManager

Coordinates the entire memory workflow.

Responsibilities:

- Save new memories
- Coordinate memory writing
- Trigger background tasks
- Update runtime state

The manager never accesses the database directly.

---

## PromptBuilder

Builds the final prompt sent to the LLM.

Future context sources include:

- Short Memory
- Summary Memory
- Vector Memory
- Tool Context

---

## MemoryExtractor

Extracts structured memories from the conversation.

Output:

```python
Memory
```

---

## MemoryRetriever

Searches similar memories from the vector database.

Responsibilities:

- Semantic search
- Retrieve all memories
- Memory count
- Convert database records into Memory objects

---

## MemoryValidator

Determines how a new memory should be handled.

Output:

```python
ValidationResult
```

Possible actions:

- ADD
- UPDATE
- MERGE
- IGNORE

---

## MemoryWriter

Applies validated changes to the database.

Responsibilities:

- Add memory
- Update memory
- Delete memory

The writer never performs business decisions.

---

## RuntimeScheduler

Determines whether background maintenance tasks should run.

Current strategy:

- Reflection interval
- Number of new memories since last reflection

---

## MemoryReflection

Optimizes the entire memory collection.

Responsibilities:

- Merge duplicated memories
- Remove outdated memories
- Generate abstract memories
- Improve long-term memory quality

Output:

```python
ReflectionResult
```

---

## VectorStore

Provides low-level database operations.

Responsibilities:

- Add
- Update
- Delete
- Query
- Count

Current implementation:

- ChromaDB

The rest of the system never communicates with ChromaDB directly.

---

## RuntimeState

Stores the runtime status of the memory engine.

Current fields include:

- memory_count
- last_reflection_time
- memory_count_after_reflection
- reflection_count

Future versions will persist RuntimeState using SQLite.

---

# Current Workflow

```text
User

↓

PromptBuilder

↓

LLM

↓

Assistant Response

↓

MemoryExtractor

↓

MemoryRetriever

↓

MemoryValidator

↓

MemoryWriter

↓

RuntimeScheduler

↓

MemoryReflection (optional)

↓

MemoryWriter
```

---

# Design Principles

The project follows several design principles.

## Single Responsibility

Each module performs only one task.

Examples:

- Retriever only retrieves.
- Validator only validates.
- Writer only writes.

---

## Layered Architecture

```text
Manager

↓

Business Logic

↓

Persistence

↓

Database
```

Each layer depends only on the layer below it.

---

## Stateless Services

Business components remain stateless whenever possible.

Examples:

- Validator
- Retriever
- Reflection
- Scheduler

Shared runtime information is stored in RuntimeState.

---

## Extensibility

Every module can be replaced independently.

For example:

- ChromaDB → Milvus
- OpenAI → Qwen
- Reflection strategy
- Validation strategy

without changing the Manager.