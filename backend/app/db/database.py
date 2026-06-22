from collections.abc import Generator
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=ENV_FILE)


def _required_setting(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"缺少数据库配置项：{name}，请检查 {ENV_FILE.name} 文件。")
    return value


database_url = URL.create(
    drivername="mysql+pymysql",
    username=_required_setting("DB_USER"),
    password=_required_setting("DB_PASSWORD"),
    host=_required_setting("DB_HOST"),
    port=int(_required_setting("DB_PORT")),
    database=_required_setting("DB_NAME"),
    query={"charset": "utf8mb4"},
)

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """项目中所有 SQLAlchemy 模型的声明基类。"""


def get_db() -> Generator[Session, None, None]:
    """为 FastAPI 接口提供并在请求结束后关闭数据库会话。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
