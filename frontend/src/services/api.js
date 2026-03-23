import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const metricsAPI = {
  getAll:  (category = null) => api.get('/api/metrics/', { params: category ? { category } : {} }),
  create:  (data)            => api.post('/api/metrics/', data),
  update:  (id, data)        => api.put(`/api/metrics/${id}`, data),
  delete:  (id)              => api.delete(`/api/metrics/${id}`)
}

export const insightsAPI = {
  generate: (category)        => api.post('/api/insights/generate', { category }),
  getAll:   (category = null) => api.get('/api/insights/', { params: category ? { category } : {} }),

  stream: (category, onChunk, onDone, onError) => {
    const token = localStorage.getItem('token')
    const url   = `${BASE_URL}/api/insights/stream`
    fetch(url, {
      method:  'POST',
      headers: {
        'Content-Type':  'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ category })
    }).then(response => {
      const reader  = response.body.getReader()
      const decoder = new TextDecoder()

      function read() {
        reader.read().then(({ done, value }) => {
          if (done) return
          const lines = decoder.decode(value).split('\n')
          for (const line of lines) {
            if (!line.startsWith('data: ')) continue
            try {
              const data = JSON.parse(line.slice(6))
              if (data.error) { onError(data.error); return }
              if (data.done)  { onDone(data.insight); return }
              if (data.text)  { onChunk(data.text) }
            } catch {}
          }
          read()
        })
      }
      read()
    }).catch(onError)
  }
}