import apiClient from './client'

const NEWS_API_URL = '/api/news'

export function analyzeNews(data) {
  return apiClient.post(`${NEWS_API_URL}/analyze`, data)
}

export function uploadNewsFile(file) {
  const formData = new FormData()
  formData.append('file', file)
  return apiClient.post(`${NEWS_API_URL}/upload`, formData)
}
