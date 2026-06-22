from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import history, news, statistics
from app.db.database import Base, engine
from app.models import database_models  # noqa: F401


app = FastAPI(
    title="新闻内容智能摘要与标题生成系统",
    description="后端基础服务",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router)
app.include_router(history.router)
app.include_router(statistics.router)


@app.on_event("startup")
def create_database_tables() -> None:
    """应用启动时创建尚不存在的数据库表。"""
    Base.metadata.create_all(bind=engine)
