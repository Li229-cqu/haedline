from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database_models import NewsRecord
from app.models.schemas import (
    Entities,
    FileUploadResponse,
    NewsAnalyzeRequest,
    NewsAnalyzeResponse,
    QualityCheckResult,
    Summaries,
    TextInfo,
)
from app.services.preprocess_service import preprocess_text
from app.services.file_service import ALLOWED_FILE_EXTENSIONS, extract_text_from_file, save_upload_file


router = APIRouter(prefix="/api/news", tags=["新闻处理"])
MAX_UPLOAD_FILE_SIZE = 5 * 1024 * 1024


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "news api is running"}


@router.post("/upload", response_model=FileUploadResponse)
def upload_news_file(file: UploadFile = File(...)) -> dict:
    """保存单个 txt/docx 新闻文件，并返回提取出的正文。"""
    filename = Path(file.filename or "").name
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="仅支持上传 .txt 和 .docx 文件，暂不支持 PDF。")

    try:
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
    except (AttributeError, OSError) as error:
        raise HTTPException(status_code=400, detail="无法读取上传文件。") from error

    if file_size == 0:
        raise HTTPException(status_code=400, detail="上传文件内容为空。")
    if file_size > MAX_UPLOAD_FILE_SIZE:
        raise HTTPException(status_code=400, detail="单个文件大小不能超过 5MB。")

    saved_path = ""
    try:
        saved_path = save_upload_file(file)
        text = extract_text_from_file(saved_path)
    except ValueError as error:
        if saved_path:
            Path(saved_path).unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=str(error)) from error
    except OSError as error:
        if saved_path:
            Path(saved_path).unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="上传文件保存或读取失败。") from error
    finally:
        file.file.close()

    return {
        "filename": filename,
        "file_size": file_size,
        "text_length": len(text),
        "text": text,
    }


@router.post("/analyze", response_model=NewsAnalyzeResponse)
def analyze_news(
    request: NewsAnalyzeRequest,
    db: Session = Depends(get_db),
) -> NewsAnalyzeResponse:
    """清洗并保存单篇新闻，返回保持稳定的基础分析结构。"""
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="新闻正文不能为空。")

    preprocess_result = preprocess_text(request.text)
    cleaned_text = preprocess_result["cleaned_text"]
    if not cleaned_text:
        raise HTTPException(status_code=400, detail="新闻正文不能为空。")
    if len(cleaned_text) < 20:
        raise HTTPException(status_code=400, detail="新闻正文过短，无法分析")

    news_record = NewsRecord(
        original_text=preprocess_result["original_text"],
        cleaned_text=cleaned_text,
        word_count=preprocess_result["word_count"],
        sentence_count=preprocess_result["sentence_count"],
        paragraph_count=preprocess_result["paragraph_count"],
    )

    try:
        db.add(news_record)
        db.commit()
        db.refresh(news_record)
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=500, detail="新闻记录保存失败，请稍后重试。") from error

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
