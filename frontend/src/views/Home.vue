<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

import { analyzeNews, uploadNewsFile } from '../api/news'

const text = ref('')
const analyzing = ref(false)
const uploading = ref(false)
const result = ref(null)

async function handleFileChange(event) {
  const file = event.target.files?.[0]
  if (!file) return

  const suffix = file.name.slice(file.name.lastIndexOf('.')).toLowerCase()
  if (!['.txt', '.docx'].includes(suffix)) {
    ElMessage.error('仅支持上传 .txt 和 .docx 文件。')
    event.target.value = ''
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('单个文件大小不能超过 5MB。')
    event.target.value = ''
    return
  }

  uploading.value = true
  try {
    const response = await uploadNewsFile(file)
    text.value = response.data.text
    ElMessage.success(`文件上传成功，已提取 ${response.data.text_length} 个字符。`)
  } catch (error) {
    const message = error.response?.data?.detail || '文件上传失败，请确认后端服务已启动。'
    ElMessage.error(message)
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}

async function handleAnalyze() {
  if (!text.value.trim()) {
    ElMessage.warning('请输入新闻正文后再生成。')
    return
  }

  analyzing.value = true
  try {
    const response = await analyzeNews({ text: text.value })
    result.value = response.data
    ElMessage.success(`新闻分析完成，记录 ID：${response.data.news_id}`)
  } catch (error) {
    const message = error.response?.data?.detail || '调用新闻分析接口失败，请确认后端服务已启动。'
    ElMessage.error(message)
  } finally {
    analyzing.value = false
  }
}
</script>

<template>
  <section class="page-container">
    <el-card>
      <template #header>新闻文本输入</template>
      <el-input
        v-model="text"
        type="textarea"
        :rows="10"
        placeholder="请输入或粘贴一篇新闻正文"
      />
      <div class="action-row">
        <label class="upload-label">
          <el-button :loading="uploading" :disabled="analyzing" plain type="primary">
            上传 txt/docx
          </el-button>
          <input type="file" accept=".txt,.docx" :disabled="uploading || analyzing" @change="handleFileChange" />
        </label>
        <el-button type="primary" :loading="analyzing" :disabled="uploading" @click="handleAnalyze">
        开始生成
        </el-button>
      </div>
    </el-card>

    <section v-if="result" class="result-section">
      <el-card>
        <template #header>分析结果</template>
        <el-alert
          :title="`新闻记录 ID：${result.news_id}`"
          type="success"
          :closable="false"
          show-icon
        />
        <el-descriptions class="text-info" :column="3" border>
          <el-descriptions-item label="字数">{{ result.text_info.word_count }}</el-descriptions-item>
          <el-descriptions-item label="句子数">{{ result.text_info.sentence_count }}</el-descriptions-item>
          <el-descriptions-item label="段落数">{{ result.text_info.paragraph_count }}</el-descriptions-item>
        </el-descriptions>
        <h3>短摘要</h3>
        <p>{{ result.summaries.short }}</p>
        <h3>长摘要</h3>
        <p>{{ result.summaries.long }}</p>
        <h3>候选标题</h3>
        <el-tag v-for="title in result.titles" :key="title" class="title-tag">
          {{ title }}
        </el-tag>
      </el-card>
    </section>
  </section>
</template>

<style scoped>
.generate-button {
  margin-top: 16px;
}

.action-row {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.upload-label input {
  display: none;
}

.text-info {
  margin-top: 16px;
}

.title-tag {
  margin: 0 8px 8px 0;
}
</style>
