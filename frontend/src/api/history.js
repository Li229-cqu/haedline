import apiClient from './client'

const HISTORY_API_URL = '/api/history'

export function getHistoryList(params) {
  return apiClient.get(HISTORY_API_URL, { params })
}

export function getHistoryDetail(id) {
  return apiClient.get(`${HISTORY_API_URL}/${id}`)
}

export function deleteHistory(id) {
  return apiClient.delete(`${HISTORY_API_URL}/${id}`)
}
