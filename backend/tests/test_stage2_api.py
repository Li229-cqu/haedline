"""第二阶段基础接口手动测试脚本。

运行前请先在 backend 目录启动服务：uvicorn main:app --reload
"""

import sys

import requests


BASE_URL = "http://localhost:8000"
TIMEOUT_SECONDS = 10


def run_step(name, request_func):
    """执行一个 HTTP 测试步骤，并输出清晰的成功或失败信息。"""
    try:
        response = request_func()
        response.raise_for_status()
        print(f"[通过] {name}（HTTP {response.status_code}）")
        return response
    except requests.RequestException as error:
        print(f"[失败] {name}：{error}")
        raise


def main():
    print(f"开始测试后端接口：{BASE_URL}")

    ping_response = run_step(
        "新闻接口运行状态",
        lambda: requests.get(f"{BASE_URL}/api/news/ping", timeout=TIMEOUT_SECONDS),
    )
    if ping_response.json().get("message") != "news api is running":
        raise RuntimeError("新闻接口 ping 返回内容不符合预期。")

    analyze_response = run_step(
        "新闻文本分析与入库",
        lambda: requests.post(
            f"{BASE_URL}/api/news/analyze",
            json={
                "text": "这是一段用于第二阶段接口测试的新闻正文，内容长度足够用于验证文本清洗、统计和数据库入库流程。",
                "summary_type": "all",
                "title_style": "all",
            },
            timeout=TIMEOUT_SECONDS,
        ),
    )
    analyze_data = analyze_response.json()
    news_id = analyze_data.get("news_id")
    text_info = analyze_data.get("text_info", {})
    if not news_id:
        raise RuntimeError("新闻分析接口未返回 news_id。")
    if any(text_info.get(field, 0) <= 0 for field in ("word_count", "sentence_count", "paragraph_count")):
        raise RuntimeError("新闻分析接口返回的文本统计结果不正确。")
    print(f"[通过] 获取到新闻记录 ID：{news_id}")

    history_response = run_step(
        "历史记录分页查询",
        lambda: requests.get(
            f"{BASE_URL}/api/history",
            params={"page": 1, "page_size": 10},
            timeout=TIMEOUT_SECONDS,
        ),
    )
    history_data = history_response.json()
    required_fields = {"total", "page", "page_size", "items"}
    if not required_fields.issubset(history_data):
        raise RuntimeError("历史记录接口返回结构不完整。")
    print(f"[通过] 历史列表返回 {history_data['total']} 条记录。")

    print("第二阶段基础接口测试完成。")


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, RuntimeError) as error:
        print(f"测试未通过：{error}")
        sys.exit(1)
