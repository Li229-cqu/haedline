from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.file_service import ALLOWED_FILE_EXTENSIONS, extract_text_from_file, save_upload_file
from app.models.news_schemas import FileUploadResponse, NewsAnalyzeRequest, NewsAnalyzeResponse
from app.services.news_service import (
    NewsPersistenceError,
    NewsValidationError,
    analyze_and_save_news,
)


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
    """接收 HTTP 请求并委托新闻业务服务完成分析与入库。"""
    try:
        return analyze_and_save_news(request.text, db)
    except NewsValidationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except NewsPersistenceError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
