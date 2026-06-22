"""新闻分析与文件上传接口的数据结构。"""

from pydantic import BaseModel, Field


class NewsAnalyzeRequest(BaseModel):
    text: str
    summary_type: str = "all"
    title_style: str = "all"


class TextInfo(BaseModel):
    word_count: int
    sentence_count: int
    paragraph_count: int


class Entities(BaseModel):
    persons: list[str] = Field(default_factory=list)
    organizations: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    times: list[str] = Field(default_factory=list)
    numbers: list[str] = Field(default_factory=list)


class Summaries(BaseModel):
    short: str
    long: str


class QualityCheckResult(BaseModel):
    keyword_coverage: float
    entity_coverage: float
    summary_similarity: float
    title_similarity: float
    clickbait_risk: str
    factual_shift_risk: str
    suggestions: list[str] = Field(default_factory=list)


class NewsAnalyzeResponse(BaseModel):
    news_id: int
    text_info: TextInfo
    keywords: list[str]
    entities: Entities
    summaries: Summaries
    titles: list[str]
    quality_check: QualityCheckResult


class FileUploadResponse(BaseModel):
    filename: str
    file_size: int
    text_length: int
    text: str
