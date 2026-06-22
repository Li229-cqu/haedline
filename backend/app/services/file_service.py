"""新闻上传文件的保存与正文读取服务。"""

import re
import shutil
from pathlib import Path
from uuid import uuid4

from docx import Document


ALLOWED_FILE_EXTENSIONS = {".txt", ".docx"}
UPLOAD_DIRECTORY = Path(__file__).resolve().parents[3] / "data" / "uploads"


def _safe_filename(filename: str) -> str:
    """移除路径成分和特殊字符，避免用户文件名造成路径注入。"""
    basename = Path(filename or "upload").name
    safe_name = re.sub(r"[^\w.\-]", "_", basename)
    return safe_name or "upload"


def save_upload_file(file) -> str:
    """将上传文件以随机安全文件名保存到 data/uploads 目录。"""
    safe_name = _safe_filename(getattr(file, "filename", "upload"))
    suffix = Path(safe_name).suffix.lower()
    if suffix not in ALLOWED_FILE_EXTENSIONS:
        raise ValueError("仅支持上传 .txt 和 .docx 文件。")

    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    saved_path = UPLOAD_DIRECTORY / f"{uuid4().hex}{suffix}"

    # 上传前由接口将文件指针复位；这里再次复位以便服务可独立复用。
    file.file.seek(0)
    with saved_path.open("wb") as target:
        shutil.copyfileobj(file.file, target)

    return str(saved_path)


def read_txt_file(file_path: str) -> str:
    """优先以 UTF-8 读取文本文件，失败时尝试 GBK。"""
    path = Path(file_path)
    for encoding in ("utf-8", "gbk"):
        try:
            text = path.read_text(encoding=encoding)
            if not text.strip():
                raise ValueError("上传文件内容为空。")
            return text
        except UnicodeDecodeError:
            continue

    raise ValueError("无法识别 txt 文件编码，请使用 UTF-8 或 GBK 编码。")


def read_docx_file(file_path: str) -> str:
    """读取 docx 文档中的非空段落文本。"""
    try:
        document = Document(file_path)
    except Exception as error:
        raise ValueError("docx 文件读取失败，请确认文件格式正确。") from error

    text = "\n".join(paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip())
    if not text.strip():
        raise ValueError("上传文件内容为空。")
    return text


def extract_text_from_file(file_path: str) -> str:
    """根据文件扩展名提取正文；PDF 等其他格式当前不支持。"""
    path = Path(file_path)
    if not path.is_file():
        raise ValueError("上传文件不存在或保存失败。")

    suffix = path.suffix.lower()
    if suffix == ".txt":
        return read_txt_file(str(path))
    if suffix == ".docx":
        return read_docx_file(str(path))
    raise ValueError("仅支持上传 .txt 和 .docx 文件，暂不支持 PDF。")
