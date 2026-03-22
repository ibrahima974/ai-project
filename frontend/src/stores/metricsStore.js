import { defineStore } from 'pinia'
import { ref } from 'vue'
import { metricsAPI } from '../services/api'

export const useMetricsStore = defineStore('metrics', () => {
  const metrics  = ref([])
  const loading  = ref(false)
  const error    = ref(null)

  async function fetchMetrics(category = null) {
    loading.value = true
    error.value   = null
    try {
      const res     = await metricsAPI.getAll(category)
      metrics.value = res.data
    } catch (e) {
      error.value = "Impossible de charger les métriques."
    } finally {
      loading.value = false
    }
  }

  async function createMetric(data) {
    const res = await metricsAPI.create(data)
    metrics.value.unshift(res.data)
  }

  async function updateMetric(id, data) {
    const res = await metricsAPI.update(id, data)
    const idx = metrics.value.findIndex(m => m.id === id)
    if (idx !== -1) metrics.value[idx] = res.data
  }

  async function deleteMetric(id) {
    await metricsAPI.delete(id)
    metrics.value = metrics.value.filter(m => m.id !== id)
  }

  return { metrics, loading, error, fetchMetrics, createMetric, updateMetric, deleteMetric }
})