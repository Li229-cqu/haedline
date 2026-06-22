"""新闻历史记录的业务服务。"""

from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.history_schemas import (
    DeleteHistoryResponse,
    HistoryDetailResponse,
    HistoryItem,
    HistoryListResponse,
)
from app.repositories.news_repository import (
    delete_news_record,
    get_news_record,
    get_news_record_page,
)


class HistoryNotFoundError(LookupError):
    """表示指定的新闻历史记录不存在。"""


class HistoryPersistenceError(RuntimeError):
    """表示历史记录删除等数据库操作失败。"""


def get_history_list(
    db: Session,
    page: int,
    page_size: int,
    keyword: Optional[str] = None,
) -> HistoryListResponse:
    """查询并转换分页历史记录。"""
    total, records = get_news_record_page(db, page, page_size, (keyword or "").strip())
    return HistoryListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[
            HistoryItem(
                id=record.id,
                title="暂未生成标题",
                word_count=record.word_count,
                sentence_count=record.sentence_count,
                paragraph_count=record.paragraph_count,
                created_at=record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            )
            for record in records
        ],
    )


def get_history_detail(db: Session, news_id: int) -> HistoryDetailResponse:
    """查询并转换单条新闻记录详情。"""
    record = get_news_record(db, news_id)
    if record is None:
        raise HistoryNotFoundError("新闻记录不存在。")

    return HistoryDetailResponse(
        id=record.id,
        original_text=record.original_text,
        cleaned_text=record.cleaned_text or "",
        word_count=record.word_count,
        sentence_count=record.sentence_count,
        paragraph_count=record.paragraph_count,
        created_at=record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    )


def delete_history_record(db: Session, news_id: int) -> DeleteHistoryResponse:
    """删除一条新闻历史记录。"""
    record = get_news_record(db, news_id)
    if record is None:
        raise HistoryNotFoundError("新闻记录不存在。")

    try:
        delete_news_record(db, record)
    except SQLAlchemyError as error:
        db.rollback()
        raise HistoryPersistenceError("新闻记录删除失败，请稍后重试。") from error

    return DeleteHistoryResponse(message="删除成功", news_id=news_id)
