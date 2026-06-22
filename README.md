# 新闻内容智能摘要与标题生成系统

## 项目简介

本项目对单篇新闻正文进行智能处理，支持文本输入或文本文件上传，并提供文本清洗、关键词抽取、实体识别、新闻要素抽取、短摘要、长摘要、候选标题及基础一致性质量校验。结果可保存并在历史记录中查看，为新闻编辑和内容运营提供辅助参考。

第一版 MVP 聚焦单篇新闻处理闭环，优先整合预训练模型、规则方法和轻量算法，不从零训练大模型。

## 技术栈（计划）

- 前端：Vue 3、Vite、JavaScript/TypeScript、Element Plus、ECharts。
- 后端：Python、FastAPI、Pydantic、SQLAlchemy。
- NLP：预训练模型、关键词抽取与规则方法；具体模型在后续开发阶段选型。
- 数据存储：开发阶段可使用 SQLite，后续可按部署需要迁移至关系型数据库。

## 目录说明

- `backend/`：后端接口、业务服务、数据模型和数据库访问代码。
- `frontend/`：前端工程，负责文本输入、文件上传、结果展示和历史记录界面。
- `docs/`：项目需求、架构设计和开发计划等文档。
- `data/`：运行期本地数据目录，其中包含上传文件和导出结果。

## 第二阶段已完成内容

第二阶段完成了单篇新闻的后端基础业务闭环及前端基础联调：

- 文本清洗：处理多余空白、连续换行、控制字符与标点周边冗余空格。
- 段落切分与句子切分：输出基础段落、句子列表。
- 文本统计：统计字数、句子数和段落数。
- 文件上传：支持单个 `.txt`、`.docx` 文件上传与正文读取，单文件限制为 5MB。
- 新闻记录入库：新闻分析接口将原文、清洗文本与统计结果写入 MySQL。
- 历史记录列表：支持分页与关键词模糊搜索。
- 历史记录详情：可查看原始正文、清洗后文本和统计数据。
- 删除历史记录：可按新闻记录 ID 删除记录。
- 前端基础联调：首页支持输入、上传和分析；历史页支持查询、详情和删除。

## 第二阶段未完成内容

- 关键词抽取将在第三阶段完成。
- 实体识别将在第三阶段完成。
- 新闻要素抽取将在第三阶段完成。
- 摘要生成将在第四阶段完成。
- 标题生成将在第五阶段完成。
- 一致性质量校验将在第六阶段完成。

在上述能力落地前，分析接口中的关键词、实体、摘要、标题和质量校验字段均保持占位数据，以保证前后端响应结构稳定。

## 第一阶段运行方式

### 后端启动

请先确认本地 MySQL Server 已启动，并在 `backend/.env` 中填写数据库连接信息。随后在项目根目录执行：

```powershell
cd backend
uvicorn main:app --reload
```

后端默认地址为 `http://127.0.0.1:8000`。

首次运行时，请先创建虚拟环境、安装依赖并按系统激活虚拟环境：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 前端启动

另开一个终端，在项目根目录执行：

```powershell
cd frontend
npm run dev
```

前端默认地址为 `http://localhost:5173`。

首次运行前端时，请先执行 `npm install`。PowerShell 如受执行策略限制，可使用 `npm.cmd install` 与 `npm.cmd run dev`。

### 后端测试

启动后端服务后，另开一个终端执行：

```powershell
cd backend
python tests/test_stage2_api.py
```

该脚本会测试新闻接口运行状态、新闻文本分析与入库、历史记录分页查询，并新增一条测试新闻记录。

### 接口测试地址

- `http://127.0.0.1:8000/docs`：Swagger 接口文档。
- `http://127.0.0.1:8000/api/news/ping`：新闻接口运行状态。
- `http://127.0.0.1:8000/api/history/ping`：历史接口运行状态。
- `http://127.0.0.1:8000/api/statistics/ping`：统计接口运行状态。
- `POST http://127.0.0.1:8000/api/news/analyze`：新闻分析、文本预处理与入库接口。

### MySQL 检查方式

在 MySQL Workbench 中连接本地 MySQL Server 后执行：

```sql
USE news_summary_system;
SHOW TABLES;
SELECT * FROM news_records ORDER BY created_at DESC;
```

`news_records` 中能看到新增记录，说明 `/api/news/analyze` 已完成文本清洗、统计并成功入库。第二阶段暂时不会向 `extraction_results`、`generation_results`、`quality_checks` 三张表写入真实数据。

### 常见问题

- **PowerShell 无法运行 `npm`**：可使用 `npm.cmd install` 和 `npm.cmd run dev`，或调整本机 PowerShell 执行策略。
- **前端调用接口失败**：确认后端已启动在 8000 端口，且前端访问地址为 `http://localhost:5173` 或 `http://127.0.0.1:5173`。
- **后端启动时数据库连接失败**：确认 MySQL Server 已启动，并检查 `backend/.env` 中的主机、端口、用户名、密码和数据库名称。
- **未看到数据表**：在 MySQL Workbench 中刷新 `news_summary_system` 的 Tables 列表，或执行 `SHOW TABLES;`。
