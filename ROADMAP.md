# AI Agent Learning Roadmap

> Goal: Build a production-style AI Agent from scratch using Python.

---

## Phase 1 — LLM Basics ✅

- [x] OpenAI SDK
- [x] Chat Completion
- [x] Streaming Output
- [x] Prompt Engineering
- [x] JSON Mode
- [x] Structured Output
- [x] Function Calling
- [x] Tool Calling

---

## Phase 2 — Conversation Memory 🚧

### Short Memory

- [x] Conversation History model
- [x] ShortMemory storage
- [x] Context Window concept
- [x] Message trimming design

### Summary Memory

- [x] Conversation summarization
- [x] Token counting
- [x] Summary prompt
- [x] SummaryMemory model

### Vector Memory

- [x] Embedding
- [x] Cosine similarity concept
- [x] Vector search
- [x] ChromaDB
- [x] SQLite Embedding Cache

### Memory Pipeline

- [x] Memory Extractor
- [x] Structured Memory / importance / category
- [x] Memory Writer and Retriever
- [x] Memory Validator and Merger
- [x] Memory Reflection
- [x] Runtime Scheduler and State Persistence

### Context and Architecture

- [x] Context Model / ContextBuilder / PromptBuilder
- [x] Token Budget and Context Compression
- [x] Memory Ranking and Score
- [x] Application Layer
- [x] Dependency Injection and Bootstrap
- [x] Repository Pattern
- [x] Infrastructure Layer

### Memory Lifecycle 🚧

- [x] `expires_at` domain model and TTL days conversion
- [x] Expiration detection and decay calculation
- [x] ACTIVE / ARCHIVED status model
- [x] Archive persistence and Chroma status filtering
- [x] Lifecycle time gate and persisted runtime state
- [ ] Memory Cleaner / physical deletion policy

### Remaining

- [ ] Session Memory
- [ ] Prompt Builder refinement

---

## Phase 3 — Agent

- [ ] Tool Router
- [ ] ReAct
- [x] Reflection
- [ ] Planning
- [ ] Workflow
- [ ] Multi-Step Reasoning

---

## Phase 4 — RAG

- [ ] Document Loader
- [ ] Chunking
- [ ] Embedding Pipeline
- [ ] Retrieval
- [ ] Reranker
- [ ] Hybrid Search

---

## Phase 5 — Multi Agent

- [ ] Planner
- [ ] Executor
- [ ] Reviewer
- [ ] Manager Agent

---

## Phase 6 — LangGraph

- [ ] StateGraph
- [ ] Memory Node
- [ ] Tool Node
- [ ] Conditional Edge

---

## Phase 7 — MCP

- [ ] MCP Client
- [ ] MCP Server
- [ ] Tool Discovery
- [ ] Remote Tool Calling
