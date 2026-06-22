"""新闻文本预处理服务。"""

from app.utils.text_utils import clean_text, count_text_info, split_paragraphs, split_sentences


def preprocess_text(text: str) -> dict:
    """完成单篇新闻的清洗、切分和基础统计，供后续服务复用。"""
    original_text = "" if text is None else (text if isinstance(text, str) else str(text))
    cleaned_text = clean_text(original_text)
    paragraphs = split_paragraphs(cleaned_text)
    sentences = split_sentences(cleaned_text)
    text_info = count_text_info(cleaned_text)

    return {
        "original_text": original_text,
        "cleaned_text": cleaned_text,
        "paragraphs": paragraphs,
        "sentences": sentences,
        "word_count": text_info["word_count"],
        "sentence_count": text_info["sentence_count"],
        "paragraph_count": text_info["paragraph_count"],
    }
