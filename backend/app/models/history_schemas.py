"""历史记录接口的数据结构。"""

from pydantic import BaseModel


class HistoryItem(BaseModel):
    id: int
    title: str
    word_count: int
    sentence_count: int
    paragraph_count: int
    created_at: str


class HistoryListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[HistoryItem]


class HistoryDetailResponse(BaseModel):
    id: int
    original_text: str
    cleaned_text: str
    word_count: int
    sentence_count: int
    paragraph_count: int
    created_at: str


class DeleteHistoryResponse(BaseModel):
    message: str
    news_id: int
