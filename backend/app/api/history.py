"""历史记录 HTTP 接口。"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.history_schemas import (
    DeleteHistoryResponse,
    HistoryDetailResponse,
    HistoryListResponse,
)
from app.services.history_service import (
    HistoryNotFoundError,
    HistoryPersistenceError,
    delete_history_record,
    get_history_detail,
    get_history_list,
)


router = APIRouter(prefix="/api/history", tags=["历史记录"])


@router.get("", response_model=HistoryListResponse)
def get_history(
    page: int = Query(1, ge=1, description="页码，从 1 开始"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    keyword: Optional[str] = Query(None, description="原文或清洗文本的搜索关键词"),
    db: Session = Depends(get_db),
) -> HistoryListResponse:
    """接收分页参数并返回历史记录列表。"""
    return get_history_list(db, page, page_size, keyword)


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "history api is running"}


@router.get("/{news_id}", response_model=HistoryDetailResponse)
def get_history_detail_by_id(
    news_id: int,
    db: Session = Depends(get_db),
) -> HistoryDetailResponse:
    """接收新闻 ID 并返回详情。"""
    try:
        return get_history_detail(db, news_id)
    except HistoryNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete("/{news_id}", response_model=DeleteHistoryResponse)
def delete_history(
    news_id: int,
    db: Session = Depends(get_db),
) -> DeleteHistoryResponse:
    """删除指定新闻记录。"""
    try:
        return delete_history_record(db, news_id)
    except HistoryNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except HistoryPersistenceError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
