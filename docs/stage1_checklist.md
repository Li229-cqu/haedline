# 第一阶段运行检查清单

本清单用于确认“新闻内容智能摘要与标题生成系统”已完成第一阶段的工程初始化、数据库基础配置和前后端模拟接口联调。

> 说明：当前项目使用 MySQL 数据库（`news_summary_system`），不使用 SQLite。因此“自动生成 SQLite 数据库文件”不适用于本项目，应改为检查 MySQL 数据库连接和数据表创建情况。

## 一、项目结构检查

- [ ] 根目录存在 `backend/` 目录。
- [ ] 根目录存在 `frontend/` 目录。
- [ ] 根目录存在 `docs/` 目录。
- [ ] 存在 `data/uploads/` 目录。
- [ ] 存在 `data/exports/` 目录。

## 二、后端运行检查

- [ ] 可以进入 `backend/` 目录。
- [ ] 已创建并激活 Python 虚拟环境。
- [ ] 执行 `pip install -r requirements.txt` 后依赖安装成功。
- [ ] 执行 `uvicorn main:app --reload` 后服务正常启动。
- [ ] 可访问 `GET http://127.0.0.1:8000/api/news/ping`。
- [ ] 可访问 `GET http://127.0.0.1:8000/api/history/ping`。
- [ ] 可访问 `GET http://127.0.0.1:8000/api/statistics/ping`。
- [ ] 可通过 `POST http://127.0.0.1:8000/api/news/analyze` 提交新闻文本并获得模拟结果。
- [ ] 可访问 `http://127.0.0.1:8000/docs` 查看自动生成的接口文档。

用于测试新闻分析接口的请求体示例：

```json
{
  "text": "这里是一段用于第一阶段联调的新闻正文。",
  "summary_type": "all",
  "title_style": "all"
}
```

## 三、数据库检查

- [ ] `backend/.env` 已正确填写本地 MySQL Server 的主机、端口、用户名、密码和数据库名称。
- [ ] MySQL Server 已启动，且可通过 MySQL Workbench 连接。
- [ ] 启动后端后，数据库 `news_summary_system` 可正常连接。
- [ ] 后端启动时自动创建以下四张表（若不存在）：
  - [ ] `news_records`（`NewsRecord`）
  - [ ] `extraction_results`（`ExtractionResult`）
  - [ ] `generation_results`（`GenerationResult`）
  - [ ] `quality_checks`（`QualityCheck`）

可在 MySQL Workbench 中执行以下 SQL 验证：

```sql
USE news_summary_system;
SHOW TABLES;
```

## 四、前端运行检查

- [ ] 可以进入 `frontend/` 目录。
- [ ] 执行 `npm install` 或 `npm.cmd install` 后依赖安装成功。
- [ ] 执行 `npm run dev` 或 `npm.cmd run dev` 后 Vite 开发服务器正常启动。
- [ ] 浏览器可访问首页 `http://localhost:5173`。
- [ ] 后端运行时，首页输入新闻文本后可以调用 `/api/news/analyze` 接口。
- [ ] 首页能够展示接口返回的模拟短摘要、长摘要和候选标题。

## 五、文档检查

- [ ] [requirements.md](requirements.md) 已完成。
- [ ] [architecture.md](architecture.md) 已完成。
- [ ] [development_plan.md](development_plan.md) 已完成。
- [ ] [api.md](api.md) 已完成。
- [ ] 本检查清单已完成并可用于验收。

## 六、第一阶段完成标准

满足以下条件即可判定第一阶段完成：

- [ ] 项目基础目录和前后端工程结构完整。
- [ ] 后端可以启动，并提供基础测试接口和新闻分析模拟接口。
- [ ] MySQL 数据库可连接，且四张基础表已创建。
- [ ] 前端可以启动并访问首页。
- [ ] 前端能够调用后端模拟接口并展示摘要和候选标题。
- [ ] 需求、架构、开发计划和接口文档完整。
- [ ] 项目已具备进入文本预处理和 NLP 功能开发阶段的基础条件。
