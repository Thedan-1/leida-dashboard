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
2) 终端进入此目录：
   ```bash
   python3 server.py
   ```
3) 浏览器访问：`http://localhost:8000/dashboard_system.html`

## 常见问题
- 若看到 “Failed to fetch / CORS” 提示：必须通过 `python3 server.py` 启动后访问，不要直接双击 HTML。
- AI 无响应：检查终端是否有 400/401 报错；必要时重启 `server.py` 并刷新页面 (Cmd+Shift+R)。
