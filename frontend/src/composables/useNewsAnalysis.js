import { ref } from 'vue'
import { ElMessage } from 'element-plus'

import { analyzeNews, uploadNewsFile } from '../api/news'


export function useNewsAnalysis() {
  const text = ref('')
  const result = ref(null)
  const analyzing = ref(false)
  const uploading = ref(false)

  async function uploadFile(file) {
    if (!file) return

    const suffix = file.name.slice(file.name.lastIndexOf('.')).toLowerCase()
    if (!['.txt', '.docx'].includes(suffix)) {
      ElMessage.error('仅支持上传 .txt 和 .docx 文件。')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      ElMessage.error('单个文件大小不能超过 5MB。')
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
    }
  }

  async function analyze() {
    if (!text.value.trim()) {
      ElMessage.warning('请输入新闻正文后再开始分析。')
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

  return { text, result, analyzing, uploading, uploadFile, analyze }
}
