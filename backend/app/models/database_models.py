from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class NewsRecord(Base):
    """单篇新闻及其处理结果的主记录。"""

    __tablename__ = "news_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    cleaned_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sentence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    paragraph_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    extraction_result: Mapped[Optional["ExtractionResult"]] = relationship(
        back_populates="news", uselist=False
    )
    generation_result: Mapped[Optional["GenerationResult"]] = relationship(
        back_populates="news", uselist=False
    )
    quality_check: Mapped[Optional["QualityCheck"]] = relationship(
        back_populates="news", uselist=False
    )


class ExtractionResult(Base):
    """新闻中的关键词、实体与新闻要素抽取结果。"""

    __tablename__ = "extraction_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    news_id: Mapped[int] = mapped_column(ForeignKey("news_records.id"), unique=True, nullable=False)
    keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    persons: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    organizations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    locations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    times: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    numbers: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    events: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    news: Mapped[NewsRecord] = relationship(back_populates="extraction_result")


class GenerationResult(Base):
    """新闻摘要与候选标题生成结果。"""

    __tablename__ = "generation_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    news_id: Mapped[int] = mapped_column(ForeignKey("news_records.id"), unique=True, nullable=False)
    short_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    long_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    title_candidates: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    final_title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    final_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    news: Mapped[NewsRecord] = relationship(back_populates="generation_result")


class QualityCheck(Base):
    """摘要和标题的基础一致性质量校验结果。"""

    __tablename__ = "quality_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    news_id: Mapped[int] = mapped_column(ForeignKey("news_records.id"), unique=True, nullable=False)
    keyword_coverage: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    entity_coverage: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    summary_similarity: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    title_similarity: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    clickbait_risk: Mapped[str] = mapped_column(String(50), default="unknown", nullable=False)
    factual_shift_risk: Mapped[str] = mapped_column(String(50), default="unknown", nullable=False)
    suggestions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    news: Mapped[NewsRecord] = relationship(back_populates="quality_check")
