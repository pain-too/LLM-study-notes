# LLM-Research-Assistant

一个面向植物香气注意力实验场景的 LLM 应用，能根据实验需求生成可直接运行的数据分析脚本，解决科研数据处理与统计分析问题。

---

## ✨ 项目亮点
- **从头搭建 LLM 交互式对话系统**
  基于 LangChain 构建完整对话链路，包含 Prompt 模板、模型调用、历史管理等核心流程。

- **对话历史本地文件持久化**
  继承 `BaseChatMessageHistory`父类，实现 `FileChatMessageHistory`，将对话记录保存为 JSON 文件，程序重启后上下文不丢失。

- **流式输出优化交互体验**
  实现逐字实时输出，解决回复卡顿、截断问题，模拟真实对话的流畅感。

- **解决多行输入被自动截断问题**
  通过内层循环读取用户输入，以 `end` 作为结束标志，支持完整段落式提问，突破单行输入限制。

- **完善的异常处理与边界控制**
  加入输入判空、异常捕获、优雅退出机制，提升程序稳定性与用户体验。

- **面向科研场景的定制化 Prompt**
  针对 Stroop 任务、舒尔特方格等实验数据，设计专业提示词，可直接生成数据清洗、统计检验、可视化代码。

---

## 🛠️ 技术栈
- Python 3.14
- LangChain
- Prompt Enginerring
- Pandas
- Matplotlib / Seaborn
- Git & GitHub

---

## 📁 项目结构
```
LLM-Research-Assistant/
├── core_langchain_chat.py     # 主程序文件
├── requirements.txt           # 项目依赖清单
├── README.md                  # 项目说明文档
└── .gitignore                 # Git 忽略规则配置文件
```
