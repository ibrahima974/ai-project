import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
})

export const metricsAPI = {
  getAll:   (category = null) => api.get('/api/metrics/', { params: category ? { category } : {} }),
  create:   (data)            => api.post('/api/metrics/', data),
  update:   (id, data)        => api.put(`/api/metrics/${id}`, data),
  delete:   (id)              => api.delete(`/api/metrics/${id}`)
}

export const insightsAPI = {
  generate: (category)  => api.post('/api/insights/generate', { category }),
  getAll:   (category = null) => api.get('/api/insights/', { params: category ? { category } : {} })
}