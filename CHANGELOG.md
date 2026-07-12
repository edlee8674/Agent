# Changelog

All notable changes to this project will be documented here.

---

## v0.1.0

Initial project.

### Features

- OpenAI Chat Completion
- Streaming Output
- Prompt Engineering

---

## v0.2.0

Conversation Memory

### Added

- Short Memory
- Token Counter
- Message Trimming

---

## v0.3.0

Summary Memory

### Added

- Conversation Summary
- Token Compression
- Automatic Summarization

---

## v0.4.0

Vector Memory

### Added

- Embedding
- Cosine Similarity
- Vector Search
- ChromaDB

---

## v0.5.0

Memory Extraction

### Added

- Memory Extractor
- Importance Score
- Memory Category
- TTL

---

## v0.6.0

Memory Storage

### Added

- Memory Writer
- Save Memory
- Update Memory
- Memory Deduplication

---

## v0.7.0

Memory Architecture Refactoring

### Refactored

- Introduced `Memory` dataclass
- Split Retriever layer
- Split Vector Store layer
- Simplified Manager layer
- Separated business logic from storage

---

## v0.8.0

Embedding Cache

### Added

- SQLite Embedding Cache
- Persistent Embedding Storage

### Improved

- Reduced Embedding API Calls
- Faster Startup
- Automatic Cache Lookup

---

## v0.9.0

Memory Validation Pipeline

### Added

- MemoryAction
- ValidationResult
- MemoryValidator
- MemoryMerger

### Refactored

- Introduced LLM-based memory validation
- Manager becomes Pipeline Orchestrator
- Writer focuses on database operations only
- Merger is responsible for memory consolidation
- Unified Chat & Embedding APIs in `llm.py`

### Pipeline

```
Extractor
    ↓
Retriever
    ↓
Validator
    ↓
ValidationResult
    ↓
Merger (optional)
    ↓
Writer
```

---

## Next Version

Memory Reflection

### Planned

- Memory Reflection
- ReflectionResult
- Memory Compression
- Memory Consolidation
- Importance Evolution
- Automatic Memory Cleanup

---

## Future Roadmap

- Prompt Builder
- TTL Scheduler
- Memory Cleaner
- Reranker
- Hybrid Search
- Agent Workflow
- Tool Calling
- Multi-Agent