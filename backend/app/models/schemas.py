"""兼容导出模块。

新代码应按领域从 news_schemas 或 history_schemas 导入；保留本模块避免已有调用中断。
"""

from app.models.history_schemas import (
    DeleteHistoryResponse,
    HistoryDetailResponse,
    HistoryItem,
    HistoryListResponse,
)
from app.models.news_schemas import (
    Entities,
    FileUploadResponse,
    NewsAnalyzeRequest,
    NewsAnalyzeResponse,
    QualityCheckResult,
    Summaries,
    TextInfo,
)

__all__ = [
    "DeleteHistoryResponse",
    "Entities",
    "FileUploadResponse",
    "HistoryDetailResponse",
    "HistoryItem",
    "HistoryListResponse",
    "NewsAnalyzeRequest",
    "NewsAnalyzeResponse",
    "QualityCheckResult",
    "Summaries",
    "TextInfo",
]
