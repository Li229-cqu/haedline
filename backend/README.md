# 后端服务

本目录为新闻内容智能摘要与标题生成系统的 FastAPI 后端服务。当前仅包含应用入口、跨域配置和测试接口，不包含摘要、标题生成或实体识别等业务逻辑。

## 启动方式

在项目根目录执行以下命令：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

若使用 macOS 或 Linux，请将激活命令替换为：

```bash
source .venv/bin/activate
```

服务默认运行在 `http://127.0.0.1:8000`，自动生成的接口文档可通过 `http://127.0.0.1:8000/docs` 查看。

## 测试接口

- `GET /api/news/ping`
- `GET /api/history/ping`
- `GET /api/statistics/ping`

## 第二阶段接口测试

运行测试前，请先启动 MySQL Server，并在一个终端中启动后端服务：

```powershell
uvicorn main:app --reload
```

另开一个终端，进入 `backend` 目录后执行：

```powershell
python tests/test_stage2_api.py
```

该脚本使用 `requests` 依次测试新闻接口运行状态、新闻分析与入库、历史记录分页查询，并会新增一条测试新闻记录。
