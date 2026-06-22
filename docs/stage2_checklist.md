# 第二阶段手动测试清单

本清单用于验收第二阶段的文本预处理、文件读取、新闻入库和历史记录基础管理能力。运行接口测试前，请先启动 MySQL Server，并确认 `backend/.env` 中的连接配置正确。

## 1. 后端启动检查

- [ ] 可以进入 `backend` 目录。
- [ ] 可以执行 `uvicorn main:app --reload`。
- [ ] 可以访问 `GET /api/news/ping`。
- [ ] 可以访问 `GET /api/history/ping`。

## 2. 文本分析接口检查

- [ ] 向 `POST /api/news/analyze` 传入空文本时返回 HTTP `400`。
- [ ] 传入清洗后少于 20 个字符的文本时返回 HTTP `400`。
- [ ] 传入正常新闻文本时返回有效的 `news_id`。
- [ ] 返回的 `text_info.word_count` 大于 0。
- [ ] 返回的 `text_info.sentence_count` 大于 0。
- [ ] 返回的 `text_info.paragraph_count` 大于 0。
- [ ] MySQL 的 `news_records` 表中新增对应记录。

## 3. 文件上传接口检查

- [ ] 上传 `.txt` 文件成功，并返回正文内容。
- [ ] 上传 `.docx` 文件成功，并返回正文内容。
- [ ] 上传空文件时返回 HTTP `400`。
- [ ] 上传不支持的文件格式时返回 HTTP `400`。
- [ ] 上传大于 5MB 的文件时返回 HTTP `400`。
- [ ] 上传接口不会直接在 `news_records` 表中创建新闻记录。

## 4. 历史记录接口检查

- [ ] `GET /api/history?page=1&page_size=10` 返回 `total`、`page`、`page_size` 和 `items` 分页数据。
- [ ] `GET /api/history/{news_id}` 返回对应新闻详情。
- [ ] 查询不存在的 `news_id` 时返回 HTTP `404`。
- [ ] 删除存在记录 `DELETE /api/history/{news_id}` 成功。
- [ ] 删除不存在记录时返回 HTTP `404`。

## 5. MySQL Workbench 检查

在 MySQL Workbench 中连接本地 MySQL Server 后执行：

```sql
USE news_summary_system;
SELECT * FROM news_records ORDER BY created_at DESC;
```

- [ ] 能看到新闻分析接口新增的记录。
- [ ] 记录包含原始正文、清洗后正文、字数、句子数、段落数和创建时间。

## 6. 自动化辅助测试

启动后端服务后，在另一个终端执行：

```powershell
cd backend
python tests/test_stage2_api.py
```

脚本依次测试新闻接口运行状态、新闻分析与入库、历史记录分页查询。脚本会创建一条用于测试的新闻记录，便于在 MySQL Workbench 中核对；不会自动删除该记录。

## 7. 第二阶段完成标准

- [ ] 后端服务、MySQL 数据库连接和基础 ping 接口均可运行。
- [ ] 新闻正文可完成清洗、统计并写入 `news_records`。
- [ ] `.txt` 和 `.docx` 文件可以单独上传和读取正文。
- [ ] 历史记录列表、详情和删除接口均可正常使用。
- [ ] 接口返回结构与 Pydantic Schema、`docs/api.md` 保持一致。
- [ ] 本清单的核心手动测试与脚本测试均通过。
