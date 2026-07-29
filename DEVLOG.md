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


# Sprint 02
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



# Sprint 03
Date

2026-07-14

Theme

- Memory Reflection
- Runtime Scheduler
- Reflection Workflow

---

## Background

加入记忆反思功能，用来压缩、提取、简化记忆，防止随着angent使用，记忆越来越多
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

Reflections(Optional)

VectorDB
```

---

## Problems

### Dependency Management
Manager 现在持有真正的 RuntimeState() 与 RuntimeScheduler() 实例，不再把 state / scheduler 模块当对象使用
```
runtime_state = RuntimeState()
runtime_scheduler = RuntimeScheduler()
memory_reflection = MemoryReflection()
```


### MemoryAction 增加 DELETE，避免 Reflection 解析 DELETE 操作时报 KeyError


### 修复 collections.get() 的扁平结构解析；此前 Retriever 仅能解析 query() 的嵌套结构，Reflection 获取全部记忆时会出错

query() 是“对一个或多个查询向量分别返回结果”，所以结果多了一层“第几个查询”的嵌套。即使只查询一个向量，也会有外层列表：

```
collections.query(query_embeddings=[embedding])
```
示例结果：

```
{
    "ids": [
        ["id-1", "id-2"]
    ],
    "documents": [
        ["用户计划去京都定居", "用户喜欢日本文化"]
    ],
    "metadatas": [
        [
            {"category": "plan", "importance": 0.8, "created_time": "2026-07-14"},
            {"category": "preference", "importance": 0.7, "created_time": "2026-07-14"},
        ]
    ],
    "distances": [
        [0.12, 0.34]
    ],
}
```
这里的第一层 [...] 对应“第 0 个查询向量”；第二层才是这个查询向量命中的 Memory 列表。因此原来的写法适用于它：
```
collection["ids"][0][i]
collection["documents"][0][i]
collection["metadatas"][0][i]
collection["distances"][0][i]
```

而 get() 不是向量检索，它只是直接取出 Collection 中的记录，没有“第几个查询向量”这一层，也没有距离：
```
collections.get()
```

示例结果：
```
{
    "ids": ["id-1", "id-2"],
    "documents": ["用户计划去京都定居", "用户喜欢日本文化"],
    "metadatas": [
        {"category": "plan", "importance": 0.8, "created_time": "2026-07-14"},
        {"category": "preference", "importance": 0.7, "created_time": "2026-07-14"},
    ],
}

简而言之,query()返回的是二维数组,get()返回的是一维数组，并且没有distances
```

## Reflection

开始不断丰富企业级Agent项目的业务逻辑，这次加的是
- Memory Validator
- ValidationResult
- MemoryAction

# Sprint 04

Date

2026-07-15

Theme

Runtime State Persistence

---

## Background

Reflection Scheduler 需要记录上次反思时间、当前记忆数量和反思次数。

如果状态只保存在内存中，程序重启后这些数据会丢失，
Scheduler 无法依据上次运行结果继续判断是否应执行 Reflection。

因此新增 `RuntimeStateStore`，使用 SQLite 持久化 `RuntimeState`。

---

## Decisions

Manager 持有状态存储实例，并在启动时恢复状态：

```
runtime_store = RuntimeStateStore()
runtime_state = runtime_store.load()
```

Reflection 的职责拆分为：

```
reflect_memory(memories)
    ↓
Reflection + Writer.apply

run_reflection()
    ↓
获取全部记忆
更新 RuntimeState
保存 RuntimeState
```

`run_reflection()` 使用 Manager 中唯一的 `runtime_state`，
不再接收重复的 `state` 参数。

---

## Problems

### SQLite 常量不是 SQL 列名

初始查询写为：

```
WHERE id = RUNTIME_ID
```

SQLite 会把 `RUNTIME_ID` 当作列名，导致：

```
sqlite3.OperationalError: no such column: RUNTIME_ID
```

修复为参数化查询：

```
cursor = self.conn.execute(
    "SELECT ... FROM runtime_state WHERE id = ?",
    (RUNTIME_ID,),
)
row = cursor.fetchone()
```

`fetchone()` 属于 cursor，不属于 SQLite connection。

---

### RuntimeState 只保存数据

初始代码调用：

```
runtime_state.save(runtime_state)
```

`RuntimeState` 是 dataclass，只表示状态数据，
不负责数据库操作。

因此改为由 Store 持久化：

```
runtime_store.save(runtime_state)
```

每次保存 Memory 后，如果本次没有触发 Reflection，
也保存更新后的 `memory_count`，保证重启后状态仍然一致。

---

### 关闭的是 Store 实例

`main.py` 最初导入的是 `runtime.state_store` 模块，
不能直接调用：

```
state_store.close()
```

应关闭 Manager 创建的实例：

```
runtime_store.close()
```

# Sprint 05

Date

2026-07-21

Theme

Application Layer

---

## Background

随着 Validator、Merger、Reflection、Scheduler 和 Runtime State 增加，
旧的 `manager.py` 同时承担了查询、写入、状态更新和持久化。

Manager 已经不再只是协调入口，而是在直接创建外部客户端、调用业务规则和保存状态。

因此开始 Application Layer 重构：

- `memory/application.py` 负责 Memory 用例流程。
- `runtime/application.py` 负责 Runtime State 用例流程。
- Bootstrap 统一创建外部依赖并注入业务组件。

---

## Decisions

### Application 负责流程编排

`MemoryApplication` 统一编排：

```text
Build Context
Save Memory
Run Reflection
Close Runtime Store
```

`RuntimeApplication` 统一编排：

```text
Load State
Refresh Memory Count
Should Reflect
Update Reflection State
Persist State
```

这样 `main.py` 只保留程序入口职责。

---

### 有外部依赖的组件使用 class

这次将持有 API、Chroma 或 SQLite 依赖的模块改为 class：

```text
LLMClient
MemoryRepository
MemoryRetriever
MemoryWriter
MemoryExtractor
MemoryValidator
MemoryMerger
MemoryReflection
```

纯数据或纯规则保持简单：

```text
Memory
MemoryAction
MemoryOperation
ReflectionResult
RuntimeState
RuntimeScheduler
format_vector_memory
```

业务组件不再自行创建 OpenAI client 或 Chroma client，
而是接收 Bootstrap 创建好的依赖。

---

## Problems

### Application 初始化引用了不存在的类

最初的 `MemoryApplication` 写为：

```python
self.writer = Writer()
self.retriever = Retriever()
self.merger.merge_memory(...)
```

但项目中只有函数式 Writer/Retriever，也没有初始化 `self.merger`，
会在创建 Application 时发生 `NameError` 或 `AttributeError`。

修复后由 Bootstrap 创建明确的依赖图：

```python
llm = LLMClient(EmbeddingCache())
repository = MemoryRepository()
writer = MemoryWriter(llm, repository)
retriever = MemoryRetriever(llm, repository)
merger = MemoryMerger(llm)

MemoryApplication(
    llm=llm,
    retriever=retriever,
    writer=writer,
    merger=merger,
    ...,
)
```

---

### 单元素 tuple 导致 LLMClient 调用失败

注入 LLM 后，`MemoryApplication` 中曾写成：

```python
self.llm = llm,
```

末尾逗号会创建单元素 tuple，因此主程序调用：

```python
memory_app.llm.chat(messages)
```

会报：

```text
AttributeError: 'tuple' object has no attribute 'chat'
```

修复为：

```python
self.llm = llm
```

---

### 不在模块导入时加载 Tokenizer

`summary_memory.py` 原本在模块顶层执行：

```python
encoding = tiktoken.get_encoding("cl100k_base")
```

当本地缺少编码缓存时，导入模块会触发网络下载；即使当前流程不使用 Summary Memory，
也可能因此无法启动或运行测试。

现在仅在 `count_tokens()` 被调用时加载编码，避免与当前 Memory Application 的启动过程耦合。

---

### Repository 接口与 Chroma 实现分离

原来的 `vector_store.py` 名为 Repository，但直接创建 Chroma client、生成 embedding 并调用 Collection。

这次拆分为：

```text
memory/repository.py
    MemoryRepository（领域数据访问接口）

infrastructure/chroma_repository.py
    ChromaMemoryRepository（Chroma 实现）

infrastructure/embedding_service.py
    EmbeddingService（Embedding 与缓存）
```

接口接收领域对象：

```python
repository.add_memory(memory)
repository.update_memory(memory_id, memory)
repository.query_memory(text)
```

具体的 `ChromaMemoryRepository` 再调用 `EmbeddingService`，将 `Memory` 转换为 Chroma 字段。

Bootstrap 必须创建并注入 `EmbeddingService`：

```python
embedding_service = EmbeddingService(llm.client, embedding_cache)
repository = ChromaMemoryRepository(embedding_service)
```

遗漏这个构造参数会导致：

```text
TypeError: ChromaMemoryRepository.__init__() missing 1 required positional argument: 'embedding_service'
```

---

### Runtime Layer 不反向依赖 Memory Layer

`RuntimeApplication` 最初直接导入 Retriever 来统计 Memory 数量。

这会让 Runtime Application 反向依赖 Memory Application 相关模块，
并增加未来循环依赖的风险。

因此改为：

```python
runtime.refresh_memory_count(
    retriever.count_memories()
)
```

MemoryApplication 负责取得数量，RuntimeApplication 只保存该数量。

---

### Reflection 状态更新顺序

Reflection 会新增、更新或删除 Memory。

因此必须在 Reflection 写入完成后重新统计 Memory 数量，
再将该值记录为 `memory_count_after_reflection`。

```text
Reflection Write
    ↓
Refresh Memory Count
    ↓
after_reflection
```

---

## Verification

- 使用 Fake LLM、Repository 与 Runtime 验证 `MemoryApplication` 保存与反思编排。
- 验证 Application 模块可正常导入。
- 验证全项目 Python 编译。
- 验证 Bootstrap 创建的 `MemoryApplication.llm` 是 `LLMClient`，而不是 tuple。

# Sprint 06

Date

2026-07-30

Theme

Context Model, ContextBuilder and PromptBuilder

---

## Background

此前 MemoryApplication 直接把向量记忆拼接成 system message。

随着 Short Memory、Summary Memory 与其他上下文来源出现，
Application 不应继续负责上下文的数据结构和 Prompt 文本格式。

因此引入 Context Model、ContextBuilder 与 PromptBuilder。

---

## Decisions

上下文构建拆分为两个阶段：

```text
ContextBuilder
    ↓
Context
    ↓
PromptBuilder
    ↓
LLM messages
```

`ContextBuilder` 只负责收集数据：

- 用户输入
- 向量检索结果
- Short Memory
- Summary Memory

`PromptBuilder` 只负责将 `Context` 格式化为 system / user messages。

MemoryApplication 接收两个 Builder，并提供：

```python
build_context(user_input)
build_prompt(context)
```

这样 `main.py` 只调用 Application 方法，不直接访问 Builder 的内部对象。

---

## Problems

### Bootstrap 与 Application 构造参数不同步

Bootstrap 已经注入：

```python
context_builder=context_builder
prompt_builder=prompt_builder
```

但 MemoryApplication 构造函数尚未声明这两个参数，导致：

```text
TypeError: MemoryApplication.__init__() got an unexpected keyword argument 'context_builder'
```

修复方式是让 Application 显式接收、保存并通过方法暴露这两个依赖。

---

### 不将方法当作 Builder 对象访问

初始入口代码写为：

```python
memory_app.build_context.build(user_input)
```

`build_context` 是 Application 方法，不是 ContextBuilder 实例。

改为：

```python
context = memory_app.build_context(user_input)
messages = memory_app.build_prompt(context)
```

---

### Short Memory 的消息格式

ShortMemory 保存的是 message dict，而不是字符串列表。

PromptBuilder 不能直接：

```python
"\n".join(context.short_memory)
```

需要将每条消息格式化为：

```text
role: content
```

---

## Verification

- 使用 Fake ContextBuilder 与 PromptBuilder 验证 Application 的上下文与 Prompt 编排。
- 验证短期消息字典可以正确进入 Prompt。
- 验证 Bootstrap 能创建 ContextBuilder 与 PromptBuilder。

