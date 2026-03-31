# 🤖 AI-powered GitHub Trending Agent 

> **一句话简介**：基于 DeepSeek 大模型的 GitHub 趋势自动监控助手。

本项目通过自动化流程感知 GitHub 每日热点，利用 LLM 进行语义分析，并实时推送深度评价至移动端钉钉，旨在解决开发者在信息过载环境下的技术筛选效率问题。

---

### 🌟 核心特性

* **智能分析**：不再只是搬运项目描述，而是通过 DeepSeek API 深度解析项目核心价值。
* **自动化流水线**：基于 **GitHub Actions** 实现无服务器（Serverless）定时调度。
* **安全加固**：采用环境隔离与 **Secrets Management**，确保 API Key 无泄露风险。
* **持久化记忆**：利用 JSON 进行增量数据管理，确保信息不重复、不遗漏。

### 🏗️ 技术架构

项目遵循标准的 AI Agent 开发范式：
1. **感知层 (Perception)**：调用 GitHub API 获取 Trending 数据。
2. **决策层 (Thinking)**：Prompt Engineering + 大语言模型分析。
3. **存储层 (Memory)**：轻量化 JSON 文件持久化存储历史状态。
4. **行动层 (Action)**：Webhook 协议对接企业级通讯工具。



### 🛠️ 快速开始

1. **配置环境变量**：
   - `DEEPSEEK_KEY`: 你的 DeepSeek API 密钥
   - `DINGTALK_URL`: 钉钉机器人 Webhook 链接

2. **本地运行**：
   ```bash
   pip install -r requirements.txt
   python github_agent_v2.py
