# 新闻内容智能摘要与标题生成系统接口文档（第二阶段）

## 1. 基础信息

- 后端基础地址：`http://localhost:8000`
- 接口数据格式：`application/json`；文件上传接口使用 `multipart/form-data`。
- 在线调试文档：`http://localhost:8000/docs`
- 当前阶段：已实现文本清洗、基础统计、单文件读取、新闻记录入库与历史记录管理；NLP 生成与抽取能力仍处于占位阶段。

## 2. 新闻接口

### 2.1 新闻接口运行状态

- **方法**：`GET`
- **地址**：`/api/news/ping`
- **功能**：测试新闻接口是否正常运行。

返回示例：

```json
{
  "message": "news api is running"
}
```

### 2.2 单篇新闻分析

- **方法**：`POST`
- **地址**：`/api/news/analyze`
- **功能**：接收一篇新闻正文，完成真实文本清洗与基础统计，并将原文和清洗结果写入 `news_records` 表。
- **说明**：摘要、标题、关键词、实体和一致性校验当前仍为占位数据，以保持前后端响应结构稳定。

请求头：

```text
Content-Type: application/json
```

请求体示例：

```json
{
  "text": "这里是一段新闻正文，需要至少二十个字符以上。",
  "summary_type": "all",
  "title_style": "all"
}
```

字段说明：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `text` | string | 是 | 新闻正文。不能为空，清洗后的文本长度不得少于 20 个字符。 |
| `summary_type` | string | 否 | 摘要类型，默认值为 `all`。当前阶段仅保留请求字段。 |
| `title_style` | string | 否 | 标题风格，默认值为 `all`。当前阶段仅保留请求字段。 |

返回字段说明：

| 字段 | 说明 |
| --- | --- |
| `news_id` | 数据库新闻记录 ID。 |
| `text_info` | 真实的文本统计结果，包含字数、句子数和段落数。 |
| `keywords` | 第二阶段暂为空列表。 |
| `entities` | 第二阶段各实体类别暂为空列表。 |
| `summaries` | 第二阶段为模块尚未实现的占位文本。 |
| `titles` | 第二阶段为标题模块尚未实现的占位标题。 |
| `quality_check` | 第二阶段为未校验的占位结果。 |

返回示例：

```json
{
  "news_id": 1,
  "text_info": {
    "word_count": 22,
    "sentence_count": 1,
    "paragraph_count": 1
  },
  "keywords": [],
  "entities": {
    "persons": [],
    "organizations": [],
    "locations": [],
    "times": [],
    "numbers": []
  },
  "summaries": {
    "short": "摘要生成模块将在后续阶段实现",
    "long": "长摘要生成模块将在后续阶段实现"
  },
  "titles": ["标题生成模块将在后续阶段实现"],
  "quality_check": {
    "keyword_coverage": 0,
    "entity_coverage": 0,
    "summary_similarity": 0,
    "title_similarity": 0,
    "clickbait_risk": "not_checked",
    "factual_shift_risk": "not_checked",
    "suggestions": ["一致性质量校验将在后续阶段实现"]
  }
}
```

常见错误：

- 空文本：HTTP `400`，`{"detail": "新闻正文不能为空。"}`。
- 文本过短：HTTP `400`，`{"detail": "新闻正文过短，无法分析"}`。

### 2.3 单文件上传与正文读取

- **方法**：`POST`
- **地址**：`/api/news/upload`
- **功能**：接收一个新闻文件，保存至服务器并提取正文内容。
- **请求格式**：`multipart/form-data`，文件字段名为 `file`。
- **支持格式**：`.txt`、`.docx`。
- **限制**：单文件最大 `5MB`；暂不支持 PDF；空文件和不支持的格式返回 HTTP `400`。
- **说明**：上传接口仅负责保存和读取正文，不会直接写入数据库。前端获取 `text` 后，应再调用新闻分析接口完成入库。

返回示例：

```json
{
  "filename": "test_news.docx",
  "file_size": 12345,
  "text_length": 860,
  "text": "提取出的新闻正文"
}
```

## 3. 历史记录接口

### 3.1 历史接口运行状态

- **方法**：`GET`
- **地址**：`/api/history/ping`
- **功能**：测试历史记录接口是否正常运行。

### 3.2 历史记录分页列表

- **方法**：`GET`
- **地址**：`/api/history?page=1&page_size=10`
- **功能**：按创建时间倒序返回新闻记录分页列表。
- **可选参数**：`keyword`，同时对 `original_text` 和 `cleaned_text` 进行模糊搜索。
- **说明**：第二阶段尚未生成标题，`title` 固定返回“暂未生成标题”。

返回示例：

```json
{
  "total": 1,
  "page": 1,
  "page_size": 10,
  "items": [
    {
      "id": 1,
      "title": "暂未生成标题",
      "word_count": 800,
      "sentence_count": 20,
      "paragraph_count": 5,
      "created_at": "2026-06-22 12:00:00"
    }
  ]
}
```

关键词搜索示例：

```text
GET /api/history?page=1&page_size=10&keyword=新闻
```

### 3.3 历史记录详情

- **方法**：`GET`
- **地址**：`/api/history/{news_id}`
- **功能**：根据新闻 ID 查询原始正文、清洗后文本及基础统计数据。

返回示例：

```json
{
  "id": 1,
  "original_text": "原始新闻正文",
  "cleaned_text": "清洗后正文",
  "word_count": 800,
  "sentence_count": 20,
  "paragraph_count": 5,
  "created_at": "2026-06-22 12:00:00"
}
```

记录不存在时返回 HTTP `404`。

### 3.4 删除历史记录

- **方法**：`DELETE`
- **地址**：`/api/history/{news_id}`
- **功能**：删除指定新闻记录。

返回示例：

```json
{
  "message": "删除成功",
  "news_id": 1
}
```

记录不存在时返回 HTTP `404`。

## 4. 统计接口

### 4.1 统计接口运行状态

- **方法**：`GET`
- **地址**：`/api/statistics/ping`
- **功能**：测试统计接口是否正常运行。

返回示例：

```json
{
  "message": "statistics api is running"
}
```

## 5. 第二阶段接口测试顺序

建议按照以下顺序进行手动联调：

1. `GET /api/news/ping`
2. `POST /api/news/upload`
3. `POST /api/news/analyze`
4. `GET /api/history`
5. `GET /api/history/{news_id}`
6. `DELETE /api/history/{news_id}`

上传成功后，将上传接口返回的 `text` 作为新闻分析接口的 `text` 参数提交；分析接口返回的 `news_id` 用于后续详情查询和删除测试。

## 6. 第三阶段计划接口与字段

- **关键词抽取接口或字段**：为新闻分析响应补充真实 `keywords` 数据，并支持关键词的重要性或权重信息。
- **实体识别字段**：填充 `entities` 中的人物、机构、地点、时间和数字等实体列表。
- **新闻要素抽取字段**：新增或补充新闻主体、事件、时间、地点等结构化新闻要素字段。

后续实现应优先复用当前响应结构；若新增字段，应同步更新 Pydantic Schema、后端接口文档和前端类型定义。
