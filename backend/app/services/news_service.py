"""单篇新闻分析的业务编排服务。"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.news_schemas import (
    Entities,
    NewsAnalyzeResponse,
    QualityCheckResult,
    Summaries,
    TextInfo,
)
from app.repositories.news_repository import create_news_record
from app.services.preprocess_service import preprocess_text


class NewsValidationError(ValueError):
    """表示新闻正文不满足基础分析要求。"""


class NewsPersistenceError(RuntimeError):
    """表示新闻记录无法写入数据库。"""


def analyze_and_save_news(text: str, db: Session) -> NewsAnalyzeResponse:
    """完成预处理、新闻记录入库并生成稳定的基础响应结构。"""
    if not text or not text.strip():
        raise NewsValidationError("新闻正文不能为空。")

    preprocess_result = preprocess_text(text)
    cleaned_text = preprocess_result["cleaned_text"]
    if not cleaned_text:
        raise NewsValidationError("新闻正文不能为空。")
    if len(cleaned_text) < 20:
        raise NewsValidationError("新闻正文过短，无法分析")

    try:
        news_record = create_news_record(
            db=db,
            original_text=preprocess_result["original_text"],
            cleaned_text=cleaned_text,
            word_count=preprocess_result["word_count"],
            sentence_count=preprocess_result["sentence_count"],
            paragraph_count=preprocess_result["paragraph_count"],
        )
    except SQLAlchemyError as error:
        db.rollback()
        raise NewsPersistenceError("新闻记录保存失败，请稍后重试。") from error

    # NLP 模块尚未接入，统一在业务层返回稳定的占位字段。
    return NewsAnalyzeResponse(
        news_id=news_record.id,
        text_info=TextInfo(
            word_count=preprocess_result["word_count"],
            sentence_count=preprocess_result["sentence_count"],
            paragraph_count=preprocess_result["paragraph_count"],
        ),
        keywords=[],
        entities=Entities(),
        summaries=Summaries(
            short="摘要生成模块将在后续阶段实现",
            long="长摘要生成模块将在后续阶段实现",
        ),
        titles=["标题生成模块将在后续阶段实现"],
        quality_check=QualityCheckResult(
            keyword_coverage=0,
            entity_coverage=0,
            summary_similarity=0,
            title_similarity=0,
            clickbait_risk="not_checked",
            factual_shift_risk="not_checked",
            suggestions=["一致性质量校验将在后续阶段实现"],
        ),
    )
