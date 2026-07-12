# AI Agent Architecture

## Project Structure

```
Agent/

│
├── config.py
├── embedding.py
├── embedding_cache.py
├── main.py
│
├── memory/
│   ├── extractor.py
│   ├── manager.py
│   ├── models.py
│   ├── retriever.py
│   ├── summary_memory.py
│   ├── vector_store.py
│   └── writer.py
│
├── prompt/
│
└── chromadb/
```

---

# Overall Flow

```
User

    │

    ▼

Memory Manager

    │

    ├──────────────┐

    ▼              ▼

Retriever      Short Memory

    │              │

    ▼              ▼

Vector DB     Summary Memory

    │              │

    └──────┬───────┘

           ▼

      Prompt Builder

           ▼

          LLM

           ▼

 Assistant Response

           ▼

 Memory Extractor

           ▼

 Memory Writer

           ▼

 Vector Database
```

---

# Module Responsibilities

## main.py

Program entry.

Responsibilities

- Receive user input
- Call Memory Manager
- Invoke LLM
- Invoke Memory Extractor
- Save memory

---

## manager.py

Coordinator.

Responsible for

- Build Context
- Retrieve memories
- Save memories
- Coordinate memory pipeline

Manager should not access Chroma directly.

---

## extractor.py

Convert conversation into structured memories.

Input

Conversation

Output

Memory[]

Example

```
User

↓

Extractor

↓

Memory(
    fact,
    category,
    importance,
    ttl
)
```

---

## writer.py

Responsible for writing memories.

Pipeline

```
Memory

↓

Search Similar

↓

Update?

↓

Add?

↓

Vector Store
```

---

## retriever.py

Responsible for querying memories.

Pipeline

```
User Question

↓

Embedding

↓

Vector Search

↓

Memory List

↓

Prompt
```

Retriever never updates memory.

---

## vector_store.py

Low-level database layer.

Only responsible for

- add
- update
- delete
- query

No business logic.

---

## models.py

Defines domain models.

Current

```
Memory
```

Future

```
Conversation
Message
Memory
Summary
```

---

## embedding.py

Responsible for

Text

↓

Embedding

---

## embedding_cache.py

Embedding cache.

Current

SQLite

Future

Redis

---

## summary_memory.py

Responsible for

Conversation

↓

Summary

↓

Replace history

---

# Design Principles

Current architecture follows

```
LLM

↓

Extractor

↓

Writer

↓

Vector Store

↓

Retriever

↓

Manager

↓

Prompt
```

Business logic never appears inside Vector Store.

---

# Future Architecture

```
                User

                  │

                  ▼

           Memory Manager

                  │

    ┌─────────────┼─────────────┐

    ▼             ▼             ▼

Short        Summary       Retriever

Memory       Memory

                  │

                  ▼

            Prompt Builder

                  ▼

                 LLM

                  ▼

             Memory Extractor

                  ▼

             Memory Validator

                  ▼

           Memory Deduplicator

                  ▼

             Memory Writer

                  ▼

             Vector Store
```

---

# Future Refactoring

Planned modules

```
memory/

validator.py

cleaner.py

reranker.py

ttl.py

prompt_builder.py

session.py

observer.py
```

---

# Project Goal

This project is intended as a step-by-step implementation of a production-style AI Agent, emphasizing clean architecture, maintainability, and extensibility rather than quick prototypes.