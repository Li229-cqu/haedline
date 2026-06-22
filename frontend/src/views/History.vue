<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

import { deleteHistory, getHistoryList } from '../api/history'

const router = useRouter()
const loading = ref(false)
const keyword = ref('')
const records = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)

async function fetchHistory() {
  loading.value = true
  try {
    const response = await getHistoryList({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value.trim() || undefined,
    })
    records.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    const message = error.response?.data?.detail || '获取历史记录失败，请确认后端服务已启动。'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  fetchHistory()
}

function handlePageChange(newPage) {
  page.value = newPage
  fetchHistory()
}

function handlePageSizeChange(newPageSize) {
  pageSize.value = newPageSize
  page.value = 1
  fetchHistory()
}

function viewDetail(id) {
  router.push(`/detail/${id}`)
}

async function handleDelete(id) {
  try {
    await ElMessageBox.confirm('删除后无法恢复，是否继续？', '删除历史记录', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await deleteHistory(id)
    ElMessage.success('删除成功。')
    if (records.value.length === 1 && page.value > 1) page.value -= 1
    await fetchHistory()
  } catch (error) {
    if (error === 'cancel' || error === 'close') return
    const message = error.response?.data?.detail || '删除历史记录失败。'
    ElMessage.error(message)
  }
}

onMounted(fetchHistory)
</script>

<template>
  <section class="page-container">
    <el-card>
      <template #header>历史记录</template>
      <div class="search-row">
        <el-input v-model="keyword" clearable placeholder="搜索原文或清洗后的文本" @keyup.enter="handleSearch" />
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </div>

      <el-table v-loading="loading" :data="records" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="180" />
        <el-table-column prop="word_count" label="字数" width="90" />
        <el-table-column prop="sentence_count" label="句子数" width="100" />
        <el-table-column prop="paragraph_count" label="段落数" width="100" />
        <el-table-column prop="created_at" label="创建时间" min-width="170" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="viewDetail(scope.row.id)">详情</el-button>
            <el-button link type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-row">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @current-change="handlePageChange"
          @size-change="handlePageSizeChange"
        />
      </div>
    </el-card>
  </section>
</template>

<style scoped>
.search-row {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.pagination-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
