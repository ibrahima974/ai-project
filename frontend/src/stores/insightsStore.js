import { defineStore } from 'pinia'
import { ref } from 'vue'
import { insightsAPI } from '../services/api'

export const useInsightsStore = defineStore('insights', () => {
  const insights  = ref([])
  const loading   = ref(false)
  const error     = ref(null)

  async function fetchInsights(category = null) {
    loading.value = true
    error.value   = null
    try {
      const res      = await insightsAPI.getAll(category)
      insights.value = res.data
    } catch (e) {
      error.value = "Impossible de charger les insights."
    } finally {
      loading.value = false
    }
  }

  async function generateInsight(category) {
    loading.value = true
    error.value   = null
    try {
      const res = await insightsAPI.generate(category)
      insights.value.unshift(res.data)
      return res.data
    } catch (e) {
      error.value = e.response?.data?.detail || "Erreur lors de la génération."
      throw e
    } finally {
      loading.value = false
    }
  }

  return { insights, loading, error, fetchInsights, generateInsight }
})