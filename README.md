# ai-notebook

## 目录

### 基础理论与工具
- [Section 1: AI大模型基本原理及API使用](section 1/README.md)
- Section 2: DeepSeek使用与Prompt工程
- Section 3: Cursor编程
- Section 4: Cursor数据可视化与洞察
- Section 5: 分析式AI基础
- Section 6: 不同领域的AI算法
- Section 7: 机器学习神器

### 时间序列
- Section 8: 时间序列模型
- Section 9: 时间序列AI大赛

### 神经网络与向量数据库
- Section 10: 神经网络基础与TensorFlow实战
- Section 11: Pytorch与视觉检测
- Section 12: Embeddings和向量数据库

### 进阶AI技术
- Section 13: RAG技术与应用
- Section 14: RAG的高级极强
- Section 15: Text2SQL：自助式数据报表开发
- Section 16: LangChain：多任务应用开发
- Section 17: Function Calling与智能体Agent开发
- Section 18: MCP与A2A的应用
- Section 19: Agent智能体系统的设计与应用
- Section 20: 视觉大模型与多模态理解
- Section 21: Fine-tuning技术与大模型优化

### 平台与工具
- Section 22: Coze工作原理与应用实例
- Section 23: Coze插件开发实战
- Section 24: Dify本地化部署和应用

### 项目实战
- Section 25: 项目实战：企业知识库（企业RAG大赛冠军项目）
- Section 26: 项目实战：交互式BI报表（AI量化交易助手）
- Section 27: 项目实战：AI智慧运营助手（百万客群经营）
- Section 28: 项目实战：AI搜索类应用（知乎直答）

---

## 名词解释

**Prompt**

Prompt（提示词）是指用户输入给AI大模型的一段文本或指令，用于引导模型生成期望的输出。它可以是一个问题、任务描述或上下文信息。Prompt的设计直接影响模型的理解和生成效果，是AI应用开发中的核心环节。

举例：
- 输入“请帮我写一份请假条”，模型会生成一份请假条。
- 输入“请用英文写一份简短的请假条”，模型会生成英文且简短的请假条。

通过调整Prompt内容，可以灵活控制模型的行为和输出结果。

**TensorFlow**

由Google开发的开源深度学习框架，广泛用于神经网络、机器学习模型的构建与训练，支持多平台部署。

举例：使用TensorFlow实现手写数字识别（MNIST）模型。
参考链接：[TensorFlow官方文档](https://www.tensorflow.org/)

**Pytorch**

由Meta（原Facebook）开发的开源深度学习框架，以动态图机制著称，适合学术研究和原型开发，也广泛应用于工业界。

举例：用Pytorch搭建卷积神经网络进行图像分类。
参考链接：[Pytorch官方文档](https://pytorch.org/)

**Embeddings**

指将文本、图像等高维数据通过神经网络映射为低维稠密向量的技术，便于相似度计算和下游AI任务。

举例：将“猫”和“狗”两个词通过Word2Vec转为向量后，可计算它们的相似度。
参考链接：[Word Embeddings介绍](https://tensorflow.google.cn/text/guide/word_embeddings)

**RAG（Retrieval-Augmented Generation）**

一种结合检索与生成的AI技术，先从外部知识库检索相关信息，再由大模型生成最终答案，提升准确性和可控性。

举例：用户提问“什么是量子计算？”，系统先检索百科知识，再由大模型生成答案。
参考链接：[RAG论文原文](https://arxiv.org/abs/2005.11401)

**Text2SQL**

指将自然语言问题自动转换为SQL查询语句的技术，常用于自助数据分析和智能报表系统。

举例：输入“查询2023年销售额最高的产品”，系统自动生成对应SQL语句。
参考链接：[Text2SQL综述](https://zhuanlan.zhihu.com/p/624010282)

**LangChain**

一个用于构建基于大语言模型（LLM）的多任务应用的开源框架，支持链式调用、工具集成和复杂对话流程设计。

举例：用LangChain实现多轮对话和外部工具调用的智能问答系统。
参考链接：[LangChain官方文档](https://python.langchain.com/)

**Function Calling**

指大模型能够根据用户指令自动调用外部函数或API，实现与外部系统的数据交互和自动化操作。

举例：用户输入“查一下明天北京的天气”，大模型自动调用天气API返回结果。
参考链接：[OpenAI Function Calling官方文档](https://platform.openai.com/docs/guides/function-calling)

**MCP（Multi-Chain Prompt）**

一种多链路提示词工程方法，通过多步推理和多轮交互提升大模型的复杂任务处理能力。

举例：复杂问答场景下，模型先分解任务、再多轮推理，最终给出答案。
参考链接：[MCP相关介绍](https://zhuanlan.zhihu.com/p/671964003)

**A2A（Agent to Agent）**

指多个智能体之间的协作与通信机制，实现复杂任务的分布式处理和自动化协同。

举例：一个智能体负责数据采集，另一个负责分析，二者自动协作完成任务。
参考链接：[A2A相关论文](https://arxiv.org/abs/2309.03409)

**Fine-tuning**

指在预训练大模型的基础上，利用特定领域或任务的数据进行再训练，以提升模型在特定场景下的表现。

举例：用医疗领域数据对通用大模型进行微调，使其更擅长医学问答。
参考链接：[Fine-tuning官方指南](https://platform.openai.com/docs/guides/fine-tuning)

**Coze**

一种面向大模型应用开发的智能体平台，支持插件开发、对话流程编排和多模态理解，便于快速构建AI应用。

举例：用Coze平台搭建企业内部知识问答机器人。
参考链接：[Coze官方文档](https://docs.coze.com/)

**Dify**

一个开源的AI应用开发与部署平台，支持大模型接入、知识库管理和多种AI应用场景的快速落地。

举例：用Dify搭建自定义的智能客服系统。
参考链接：[Dify官方文档](https://docs.dify.ai/)

---

## 学习建议与知识储备

### 1. AI大模型与基础理论
- 机器学习/深度学习基础（如神经网络、损失函数、优化算法）
- 主流大模型（如GPT、LLM）的基本原理与API调用

### 2. 主流AI开发框架
- TensorFlow与Pytorch的基本用法、模型训练与部署
- Embeddings（向量化表达）、向量数据库（如FAISS、Milvus）

### 3. AI应用开发与工程
- Prompt工程（Prompt Engineering）与RAG（检索增强生成）技术
- LangChain、Function Calling等大模型应用开发框架
- Fine-tuning（微调）与模型优化方法

### 4. 智能体与多智能体系统
- Agent（智能体）系统设计、A2A（Agent to Agent）协作机制
- MCP（Multi-Chain Prompt）等多链路推理方法

### 5. 数据分析与可视化
- Text2SQL（自然语言转SQL）、自助式数据报表开发
- 数据可视化工具与分析方法

### 6. 行业与场景应用
- 时间序列分析与预测
- 视觉大模型与多模态理解
- 企业知识库、智能客服、运营助手等AI项目实战

### 7. 平台与工具
- Coze、Dify等AI应用开发与部署平台
- 插件开发、API集成、知识库管理

---

#### 建议的储备方式
- 先掌握Python编程基础
- 学习主流深度学习框架（TensorFlow、Pytorch）
- 了解大模型API的基本调用方式
- 熟悉Prompt设计与RAG、LangChain等新兴AI工程技术
- 关注智能体系统与多智能体协作的基本思想
- 具备一定的数据分析、SQL和可视化能力

如需针对某一Section的详细学习建议或资料推荐，请告知具体方向，可为您定制学习路径！