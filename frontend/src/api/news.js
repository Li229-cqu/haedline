import axios from 'axios'

const NEWS_API_URL = 'http://localhost:8000/api/news'

export function analyzeNews(data) {
  return axios.post(`${NEWS_API_URL}/analyze`, data)
}

export function uploadNewsFile(file) {
  const formData = new FormData()
  formData.append('file', file)
  return axios.post(`${NEWS_API_URL}/upload`, formData)
}
