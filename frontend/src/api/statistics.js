import apiClient from './client'

export function getStatistics() {
  return apiClient.get('/api/statistics')
}
