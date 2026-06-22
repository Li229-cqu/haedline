import axios from 'axios'

export function getStatistics() {
  return axios.get('http://localhost:8000/api/statistics')
}
