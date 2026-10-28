# Leida Dashboard (工业巡检大屏)

一个包含 3D 可视化、数据管理与 AI 智能助手的工业巡检大屏示例包。

## 目录结构
- dashboard_system.html — 管理入口，含 AI 聊天、数据导入等功能
- dashboard/ — 前端资源与 3D 场景
- mock_data/ — 演示 JSON 数据
- server.py — 本地代理服务器（解决 CORS，转发 AI 请求）
- test_ai.py — ERNIE API 连通性测试
- 使用说明.md — 简体中文快速上手指南
- 项目开发报告.md — 功能与技术说明

## 本地运行
1) 安装 Python 3。
2) 终端进入此目录，先设置 AI 密钥（server.py 从环境变量读取，不再硬编码）：
   ```bash
   # Unix / macOS:
   export BAIDU_API_KEY="你的密钥"
   # Windows PowerShell:
   $env:BAIDU_API_KEY = "你的密钥"
   ```
3) 启动服务：
   ```bash
   python server.py
   ```
4) 浏览器访问：`http://localhost:8000/dashboard_system.html`

代理只接受 `/api/chat` 的 JSON 请求，限制请求体为 1 MiB，并为上游调用设置 30 秒超时。没有配置 `BAIDU_API_KEY` 时接口会明确返回 `503`，不会尝试转发空凭据。默认只允许 `http://localhost:8000` 的跨域来源；如果前端运行在其他本地端口，可通过 `LEIDA_ALLOWED_ORIGIN` 配置。

## 常见问题
- 若看到 “Failed to fetch / CORS” 提示：必须通过 `python3 server.py` 启动后访问，不要直接双击 HTML。
- AI 无响应：检查终端是否有 400/401 报错；必要时重启 `server.py` 并刷新页面 (Cmd+Shift+R)。
