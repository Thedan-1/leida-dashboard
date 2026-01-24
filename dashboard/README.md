# Dashboard 项目结构说明

## 📁 目录结构

```
dashboard/
├── frontend/           # 前端资源
│   ├── dashboard.html             # 3D可视化大屏（原始版）
│   ├── dashboard_backup.html      # 备份文件
│   └── dashboard_single_backup.html
├── backend/            # 后端服务（预留）
└── assets/             # 静态资源
    └── sample_inspection_data.json  # 示例数据
```

## 🚀 使用方法

### 打开主文件
直接在浏览器中打开根目录的 `dashboard_system.html`

### 数据导入
1. 点击左侧导航"系统设置"
2. 点击"上传巡检数据JSON文件"
3. 选择从App导出的 `Report_*.json` 文件

### 功能模块
- **数据大屏**：3D可视化+实时数据
- **巡检报告**：表格展示所有记录
- **员工管理**：人员统计卡片
- **统计分析**：图表分析
- **系统设置**：数据导入

## 📊 数据格式

App报告格式（与大屏完全兼容）：
```json
{
  "project": "锅炉房安全巡检",
  "exportTime": "2026-01-23T10:00:00Z",
  "record": {
    "id": "uuid",
    "inspector": "姓名",
    "time": "2026-01-23 10:00:00",
    "location": "位置",
    "position": {"x": 0, "y": 0, "z": 0},
    "temperature": 85.2,
    "pressure": 1.68,
    "status": "正常/告警",
    "issue": "问题描述",
    "description": "详细说明"
  }
}
```

## 🔧 技术栈

- Three.js：3D渲染
- ECharts：数据图表
- 原生JavaScript：无框架依赖

## 📝 TODO

- [ ] 添加PLY点云加载功能
- [ ] 实现WebSocket实时推送
- [ ] 后端API服务
