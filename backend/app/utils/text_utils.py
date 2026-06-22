"""新闻文本清洗、切分与基础统计工具。"""

import re
from typing import Optional


def _safe_text(text: Optional[str]) -> str:
    """将 None 等异常输入转换为空字符串，避免基础工具函数报错。"""
    if text is None:
        return ""
    if not isinstance(text, str):
        return str(text)
    return text


def clean_text(text: str) -> str:
    """清理新闻正文中的冗余空白、控制字符和标点周围空格。"""
    cleaned = _safe_text(text)
    if not cleaned:
        return ""

    # 统一换行符，并移除换行以外的不可见控制字符。
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", cleaned)

    # 合并同一行内的连续空白；连续空行最多保留一个空行。
    cleaned = re.sub(r"[ \t\f\v]+", " ", cleaned)
    cleaned = re.sub(r" *\n *", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    # 去除常见中英文标点前后的冗余空格，不改变段落换行结构。
    cleaned = re.sub(r"[ \t]*([，。！？；：、,.!?;:])[ \t]*", r"\1", cleaned)

    return cleaned.strip()


def split_paragraphs(text: str) -> list[str]:
    """按换行切分正文段落，并过滤空段落。"""
    safe_text = _safe_text(text)
    return [paragraph.strip() for paragraph in safe_text.splitlines() if paragraph.strip()]


def split_sentences(text: str) -> list[str]:
    """按中英文常用句末标点切分句子，并保留句末标点。"""
    safe_text = _safe_text(text).strip()
    if not safe_text:
        return []

    # 换行只用于组织段落，不应阻断同一句文本的识别。
    normalized = re.sub(r"\s+", " ", safe_text)
    sentences = re.findall(r"[^。！？；.!?]+[。！？；.!?]*", normalized)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def count_chinese_chars(text: str) -> int:
    """统计 CJK 基本汉字数量，不计入英文、数字和标点。"""
    return len(re.findall(r"[\u4e00-\u9fff]", _safe_text(text)))


def count_text_info(text: str) -> dict:
    """返回正文的暂定字数、句子数和段落数统计结果。"""
    safe_text = _safe_text(text)
    # 当前 word_count 使用去除空白后的总字符数，后续可替换为分词统计。
    word_count = len(re.sub(r"\s+", "", safe_text))

    return {
        "word_count": word_count,
        "sentence_count": len(split_sentences(safe_text)),
        "paragraph_count": len(split_paragraphs(safe_text)),
    }
