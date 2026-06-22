# 前端服务

本目录为新闻内容智能摘要与标题生成系统的 Vue 3 前端工程，使用 Vite 构建，并集成 Element Plus、Vue Router、Axios 与 ECharts。

## 启动方式

请在 `frontend` 目录执行：

```powershell
npm install
npm run dev
```

PowerShell 如因执行策略无法运行 `npm`，可改用：

```powershell
npm.cmd install
npm.cmd run dev
```

开发服务器默认访问地址为 `http://localhost:5173`。启动前请同时启动后端服务，以便首页调用新闻分析接口。
