from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database_models import NewsRecord
from app.models.schemas import DeleteHistoryResponse, HistoryDetailResponse, HistoryListResponse


router = APIRouter(prefix="/api/history", tags=["历史记录"])


@router.get("", response_model=HistoryListResponse)
def get_history(
    page: int = Query(1, ge=1, description="页码，从 1 开始"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    keyword: Optional[str] = Query(None, description="原文或清洗文本的搜索关键词"),
    db: Session = Depends(get_db),
) -> dict:
    """按创建时间倒序分页返回新闻记录列表。"""
    query = db.query(NewsRecord)
    search_keyword = keyword.strip() if keyword else ""
    if search_keyword:
        search_pattern = f"%{search_keyword}%"
        query = query.filter(
            or_(
                NewsRecord.original_text.like(search_pattern),
                NewsRecord.cleaned_text.like(search_pattern),
            )
        )

    total = query.count()
    records = (
        query.order_by(NewsRecord.created_at.desc(), NewsRecord.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": record.id,
                "title": "暂未生成标题",
                "word_count": record.word_count,
                "sentence_count": record.sentence_count,
                "paragraph_count": record.paragraph_count,
                "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for record in records
        ],
    }


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "history api is running"}


@router.get("/{news_id}", response_model=HistoryDetailResponse)
def get_history_detail(news_id: int, db: Session = Depends(get_db)) -> dict:
    """返回指定新闻记录的原文、清洗文本和基础统计信息。"""
    record = db.get(NewsRecord, news_id)
    if record is None:
        raise HTTPException(status_code=404, detail="新闻记录不存在。")

    return {
        "id": record.id,
        "original_text": record.original_text,
        "cleaned_text": record.cleaned_text or "",
        "word_count": record.word_count,
        "sentence_count": record.sentence_count,
        "paragraph_count": record.paragraph_count,
        "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }


@router.delete("/{news_id}", response_model=DeleteHistoryResponse)
def delete_history(news_id: int, db: Session = Depends(get_db)) -> dict:
    """删除指定新闻记录；当前阶段不查询或处理业务结果详情。"""
    record = db.get(NewsRecord, news_id)
    if record is None:
        raise HTTPException(status_code=404, detail="新闻记录不存在。")

    try:
        db.delete(record)
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="新闻记录删除失败，请稍后重试。") from error

    return {"message": "删除成功", "news_id": news_id}
