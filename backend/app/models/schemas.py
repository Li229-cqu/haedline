from pydantic import BaseModel, Field


class NewsAnalyzeRequest(BaseModel):
    """新闻分析接口的请求参数。"""

    text: str
    summary_type: str = "all"
    title_style: str = "all"


class TextInfo(BaseModel):
    """新闻正文的基础统计信息。"""

    word_count: int
    sentence_count: int
    paragraph_count: int


class Entities(BaseModel):
    """新闻中识别出的实体集合。"""

    persons: list[str] = Field(default_factory=list)
    organizations: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    times: list[str] = Field(default_factory=list)
    numbers: list[str] = Field(default_factory=list)


class Summaries(BaseModel):
    """不同长度的新闻摘要。"""

    short: str
    long: str


class QualityCheckResult(BaseModel):
    """生成结果的基础质量校验信息。"""

    keyword_coverage: float
    entity_coverage: float
    summary_similarity: float
    title_similarity: float
    clickbait_risk: str
    factual_shift_risk: str
    suggestions: list[str] = Field(default_factory=list)


class NewsAnalyzeResponse(BaseModel):
    """新闻分析接口的标准返回结构。"""

    news_id: int
    text_info: TextInfo
    keywords: list[str]
    entities: Entities
    summaries: Summaries
    titles: list[str]
    quality_check: QualityCheckResult


# 业务异常统一由 FastAPI 的 HTTPException 生成标准错误响应，无需单独定义错误模型。
class FileUploadResponse(BaseModel):
    """单文件上传并提取正文后的返回结构。"""

    filename: str
    file_size: int
    text_length: int
    text: str


class HistoryItem(BaseModel):
    """历史记录列表中的单条摘要信息。"""

    id: int
    title: str
    word_count: int
    sentence_count: int
    paragraph_count: int
    created_at: str


class HistoryListResponse(BaseModel):
    """分页历史记录列表返回结构。"""

    total: int
    page: int
    page_size: int
    items: list[HistoryItem]


class HistoryDetailResponse(BaseModel):
    """单条历史新闻记录详情结构。"""

    id: int
    original_text: str
    cleaned_text: str
    word_count: int
    sentence_count: int
    paragraph_count: int
    created_at: str


class DeleteHistoryResponse(BaseModel):
    """删除历史记录后的确认结果。"""

    message: str
    news_id: int
