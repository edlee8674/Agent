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
- [x] Structured Memory / TTL / importance / category
- [x] Memory Writer
- [x] Memory Retriever
- [x] Memory Validator
- [x] Memory Merger
- [x] Memory Reflection
- [x] Runtime Scheduler and State Persistence

### Context and Architecture

- [x] Context Model
- [x] ContextBuilder
- [x] PromptBuilder
- [x] Application Layer
- [x] Dependency Injection and Bootstrap
- [x] Repository Pattern
- [x] Infrastructure Layer

### Remaining

- [ ] Memory Cleaner
- [ ] Memory Ranking
- [ ] TTL Cleaner
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
