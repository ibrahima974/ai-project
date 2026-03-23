import { defineStore } from 'pinia'
import { ref } from 'vue'
import { insightsAPI } from '../services/api'

export const useInsightsStore = defineStore('insights', () => {
  const insights       = ref([])
  const loading        = ref(false)
  const error          = ref(null)
  const streamContent  = ref('')
  const isStreaming    = ref(false)

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

  function streamInsight(category) {
    return new Promise((resolve, reject) => {
      streamContent.value = ''
      isStreaming.value   = true
      error.value         = null

      insightsAPI.stream(
        category,
        (chunk) => { streamContent.value += chunk },
        (insight) => {
          isStreaming.value = false
          insights.value.unshift({
            id:           insight.id,
            title:        insight.title,
            content:      streamContent.value,
            category:     insight.category,
            generated_at: new Date().toISOString()
          })
          resolve(insight)
        },
        (err) => {
          isStreaming.value = false
          error.value       = err
          reject(err)
        }
      )
    })
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

  return {
    insights, loading, error,
    streamContent, isStreaming,
    fetchInsights, generateInsight, streamInsight
  }
})