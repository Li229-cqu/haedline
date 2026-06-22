<script setup>
import { onMounted, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import { getHistoryDetail } from '../api/history'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
})

const router = useRouter()
const loading = ref(false)
const detail = ref(null)

async function fetchDetail() {
  loading.value = true
  try {
    const response = await getHistoryDetail(props.id)
    detail.value = response.data
  } catch (error) {
    detail.value = null
    const message = error.response?.data?.detail || '获取新闻详情失败，请确认记录存在。'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

watch(() => props.id, fetchDetail)
onMounted(fetchDetail)
</script>

<template>
  <section class="page-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>新闻记录详情</span>
          <el-button @click="router.push('/history')">返回历史记录</el-button>
        </div>
      </template>

      <el-empty v-if="!loading && !detail" description="未找到新闻记录或加载失败。" />
      <template v-else-if="detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="记录 ID">{{ detail.id }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ detail.created_at }}</el-descriptions-item>
          <el-descriptions-item label="字数">{{ detail.word_count }}</el-descriptions-item>
          <el-descriptions-item label="句子数">{{ detail.sentence_count }}</el-descriptions-item>
          <el-descriptions-item label="段落数">{{ detail.paragraph_count }}</el-descriptions-item>
        </el-descriptions>
        <h3>原始新闻正文</h3>
        <pre class="text-content">{{ detail.original_text }}</pre>
        <h3>清洗后正文</h3>
        <pre class="text-content">{{ detail.cleaned_text }}</pre>
      </template>
    </el-card>
  </section>
</template>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.text-content {
  padding: 12px;
  overflow-wrap: anywhere;
  white-space: pre-wrap;
  background: #f5f7fa;
  border-radius: 4px;
  font-family: inherit;
  line-height: 1.7;
}
</style>
