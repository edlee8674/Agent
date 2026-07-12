# AI Agent 开发日志

> 记录每一次重要的设计、重构、踩坑和学习心得。
>
> 不记录「做了什么」，重点记录「为什么这么设计」。

---

# 2026-07-11

## 本次目标

完成 Memory 模块第一次重构。

---

## 完成内容

- 引入 ChromaDB 作为长期记忆存储
- Memory 改为 dataclass
- 新增 Retriever
- 新增 Writer
- Manager 不再直接操作 Chroma

---

## 为什么要重构

最开始整个 Memory 模块只有几个函数：

```
search_memory()

save_memory()

build_context()
```

所有逻辑都写在一起。

随着功能增加：

- Summary Memory
- Vector Memory
- TTL
- Metadata
- Deduplication

Manager 已经越来越臃肿。

因此决定拆层。

---

## 新架构

```
Manager

↓

Retriever

↓

Writer

↓

Vector Store
```

职责：

Manager

负责协调流程。

Retriever

负责查询。

Writer

负责写入。

Vector Store

负责数据库。

这样以后新增数据库（Milvus、PGVector）时，
只需要修改 Vector Store。

---

## 遇到的问题

### 1）循环引用

```
embedding.py

↓

vector_memory.py

↓

embedding.py
```

导致：

ImportError

解决：

Embedding 不再引用 Memory。

Memory 负责调用 Embedding。

---

### 2）Embedding 重复计算

发现：

一次用户输入可能计算三四次 Embedding。

解决：

新增 SQLite Cache。

以后：

```
文本

↓

SQLite

↓

没有

↓

Embedding API
```

以后可以升级 Redis。

---

### 3）Metadata 为 None

历史数据没有 metadata。

Retriever 转 Memory 时：

```
metadata["category"]
```

直接报错。

解决：

增加默认值。

以后旧数据也能兼容。

---

## 学到的内容

开始理解了：

为什么大型项目都会拆很多层。

以前觉得：

```
直接写一起最快。
```

现在发现：

维护成本会越来越高。

---

## 下一步计划

继续重构：

- Prompt Builder
- Memory Validator
- Memory Cleaner
- TTL Scheduler