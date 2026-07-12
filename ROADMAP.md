# AI Agent Learning Roadmap

> Goal:
> Build a production-style AI Agent from scratch using Python.

---

# Phase 1 - LLM Basics ✅

- [x] OpenAI SDK
- [x] Chat Completion
- [x] Streaming Output
- [x] Prompt Engineering
- [x] JSON Mode
- [x] Structured Output
- [x] Function Calling
- [x] Tool Calling

---

# Phase 2 - Conversation Memory ✅

## Short Memory

- [x] Conversation History
- [x] Token Counter
- [x] Context Window
- [x] Message Trimming

---

## Summary Memory

- [x] Conversation Summarization
- [x] Token Compression
- [x] Summary Prompt
- [x] Summary Update

---

## Vector Memory

- [x] Embedding
- [x] Cosine Similarity
- [x] Vector Search
- [x] ChromaDB

---

## Memory Extractor

- [x] Extract Facts
- [x] Importance
- [x] Category
- [x] TTL
- [x] Structured Memory

---

## Memory Writer

- [x] Save Memory
- [x] Memory Update
- [x] Deduplication
- [x] Embedding Cache

---

## Memory Retriever

- [x] Vector Search
- [x] Memory Formatting
- [x] Memory Model
- [x] Metadata Parsing

---

## Current Progress 🚧

Memory Module Refactoring

Current Architecture

Memory
    ↓
Extractor
    ↓
Retriever
    ↓
Writer
    ↓
Vector Store

Remaining

- [ ] Memory Validator
- [ ] Memory Cleaner
- [ ] Memory Ranking
- [ ] TTL Cleaner
- [ ] Memory Compression
- [ ] Session Memory
- [ ] Prompt Builder

---

# Phase 3 - Agent

- [ ] Tool Router
- [ ] ReAct
- [ ] Reflection
- [ ] Planning
- [ ] Workflow
- [ ] Multi-Step Reasoning

---

# Phase 4 - RAG

- [ ] Document Loader
- [ ] Chunking
- [ ] Embedding Pipeline
- [ ] Retrieval
- [ ] Reranker
- [ ] Hybrid Search

---

# Phase 5 - Multi Agent

- [ ] Planner
- [ ] Executor
- [ ] Reviewer
- [ ] Manager Agent

---

# Phase 6 - LangGraph

- [ ] StateGraph
- [ ] Memory Node
- [ ] Tool Node
- [ ] Conditional Edge

---

# Phase 7 - MCP

- [ ] MCP Client
- [ ] MCP Server
- [ ] Tool Discovery
- [ ] Remote Tool Calling

---

# Long-term Goal

Build a production-ready AI Agent framework.
