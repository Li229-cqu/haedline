import axios from 'axios'

const HISTORY_API_URL = 'http://localhost:8000/api/history'

export function getHistoryList(params) {
  return axios.get(HISTORY_API_URL, { params })
}

export function getHistoryDetail(id) {
  return axios.get(`${HISTORY_API_URL}/${id}`)
}

export function deleteHistory(id) {
  return axios.delete(`${HISTORY_API_URL}/${id}`)
}
