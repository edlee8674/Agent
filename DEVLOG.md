# AI Agent Development Log

> 记录项目演进过程中的设计思考、架构调整、踩坑记录和经验总结。
>
> 不记录功能列表（那是 CHANGELOG 的职责），
> 重点记录每一次迭代为什么这样设计。

---

# Sprint 01

Date

2026-07-11

Theme

Memory Architecture Refactoring

---

## Background

随着 Summary Memory、Vector Memory、Metadata 等功能增加，
Manager 已经承担了越来越多职责。

原来的实现：

```
Manager

├── Search
├── Save
├── Build Context
├── Update
└── ChromaDB
```

业务逻辑和数据库操作完全耦合。

后续继续增加 TTL、Reflection、Validator 时，
代码会越来越难维护。

因此决定开始第一次架构重构。

---

## Decisions

本次决定：

- Memory 使用 dataclass
- 拆分 Retriever
- 拆分 Writer
- Manager 只负责协调流程
- Vector Store 只负责数据库

形成新的结构：

```
Manager

↓

Retriever

↓

Writer

↓

Vector Store
```

---

## Problems

### Circular Import

最初：

```
embedding.py

↓

vector_store.py

↓

embedding.py
```

导致 ImportError。

最终：

Embedding 不再依赖 Memory。

---

### Embedding 重复计算

发现：

一次用户请求会重复计算 Embedding。

例如：

```
Retriever

↓

Writer

↓

Validator
```

每个模块都会重新调用 Embedding API。

解决：

增加 SQLite Embedding Cache。

后续可以替换为 Redis。

---

### Metadata 兼容问题

历史数据没有 metadata。

Retriever 转 Memory 时：

```
metadata["category"]
```

直接抛异常。

最终：

统一采用：

```
metadata.get(...)
```

保证兼容旧版本数据。

---

## Reflection

开始真正理解：

"拆层" 不是为了代码好看。

而是为了：

业务逻辑可以不断增长，
而不会影响底层存储。

这是第一次真正按照软件架构思路，而不是脚本思路写代码。

---

## Next Sprint

- Memory Validator
- ValidationResult
- MemoryAction


# Sprint 01
Date

2026-07-12

Theme

- Memory Validator
- ValidationResult
- MemoryAction

---

## Background

一个成熟的Agent 在管理记忆上，不是简单的提取记忆->报错记忆, 
所以加入Memory Validator判断要保存的新记忆是否合法、是否重复、是否冲突、格式是否正确

---

## Decisions
新Memory生命周期将改造成：
```
Conversation

↓

Extractor

↓

Memory

↓

Validator

↓

Writer

↓

VectorDB
```

---

## Problems

### Memory Action
定义Memory Action枚举类时，加入了@dataclass，
因为枚举类代表几个固定值，而@dataclass是给数据对象用的，以Memory类为例,在创建对象时，python会自动帮我生成
```
def __init__(self, id, fact, importance):
        self.id = id
        self.fact = fact
        self.importance = importance

def __repr__(self):

def __eq__(self):
```

Enum是自己控制对象生成，永远是那几个固定值，而dataclass会创建普通对象，可能会改掉值

### 修复 TTL 解析、缺省 TTL 的读取和 short-memory 格式化错误

为什么改成
```
metadata.get("TTL")
```
因为TTL是后面加的属性，以前的记忆没有TTL，如果写
```
metadata["TTL"]
```
如果没有TTL,一个返回None一个返回KeyError: 'ttl'

### 修复validator.py 的 f-string 示例 JSON 已将 {} 转义为 {{}}，不会再被 Python 当作格式化表达式解析。

## Reflection

开始不断丰富企业级Agent项目的业务逻辑，这次加的是
- Memory Validator
- ValidationResult
- MemoryAction

## Next Sprint

- Memory Reflection
