"""新闻记录的数据库访问层。

本模块只处理 SQLAlchemy ORM 读写，不承载 HTTP 或 NLP 业务规则。
"""

from typing import Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.database_models import NewsRecord


def create_news_record(
    db: Session,
    original_text: str,
    cleaned_text: str,
    word_count: int,
    sentence_count: int,
    paragraph_count: int,
) -> NewsRecord:
    """创建并持久化一条新闻记录。"""
    record = NewsRecord(
        original_text=original_text,
        cleaned_text=cleaned_text,
        word_count=word_count,
        sentence_count=sentence_count,
        paragraph_count=paragraph_count,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_news_record(db: Session, news_id: int) -> Optional[NewsRecord]:
    """按主键查询单条新闻记录。"""
    return db.get(NewsRecord, news_id)


def get_news_record_page(
    db: Session,
    page: int,
    page_size: int,
    keyword: str = "",
) -> Tuple[int, list[NewsRecord]]:
    """按创建时间倒序分页查询新闻记录，可按原文或清洗文本搜索。"""
    query = db.query(NewsRecord)
    if keyword:
        pattern = "%%%s%%" % keyword
        query = query.filter(
            or_(
                NewsRecord.original_text.like(pattern),
                NewsRecord.cleaned_text.like(pattern),
            )
        )

    total = query.count()
    records = (
        query.order_by(NewsRecord.created_at.desc(), NewsRecord.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return total, records


def delete_news_record(db: Session, record: NewsRecord) -> None:
    """删除指定新闻记录并提交事务。"""
    db.delete(record)
    db.commit()
